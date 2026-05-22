#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <cuda_runtime.h>

using namespace std;

typedef vector<vector<int>> Matrix;

Matrix multiply_seq(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int k = 0; k < n; ++k)
            for (int j = 0; j < n; ++j)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

__global__ void matmul_cuda(const int* A, const int* B, int* C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < n && col < n) {
        int sum = 0;
        for (int k = 0; k < n; ++k)
            sum += A[row * n + k] * B[k * n + col];
        C[row * n + col] = sum;
    }
}

void fillRandom(Matrix& mat) {
    int n = mat.size();
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            mat[i][j] = rand() % 11;
}

int* flatten(const Matrix& mat) {
    int n = mat.size();
    int* flat = new int[n * n];
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            flat[i * n + j] = mat[i][j];

    return flat;
}

int main() {
    srand((unsigned)time(nullptr));

    const int sizes[] = {200, 400, 800, 1200, 1600, 2000};
    const int num_sizes = 6;
    const int repeats = 3;

    struct BlockConfig { int tx, ty; const char* name; };
    BlockConfig configs[] = {
        {8, 8, "8x8"},
        {16, 16, "16x16"},
        {16, 32, "16x32"},
        {32, 16, "32x16"},
        {32, 32, "32x32"}
    };
    const int num_configs = 5;

    const string csv_filename = "results_cuda.csv";
    ofstream out(csv_filename);
    out << "size;block;time_sec\n";
    out.close();

    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    cout << "CUDA experiments started\n";

    for (int s = 0; s < num_sizes; ++s) {
        int n = sizes[s];
        cout << "Size: " << n << "x" << n << endl;

        Matrix A(n, vector<int>(n)), B(n, vector<int>(n));
        fillRandom(A);
        fillRandom(B);

        // Подготовка данных для GPU
        int* h_A = flatten(A);
        int* h_B = flatten(B);
        int* h_C = new int[n * n];

        int *d_A, *d_B, *d_C;
        cudaMalloc(&d_A, n * n * sizeof(int));
        cudaMalloc(&d_B, n * n * sizeof(int));
        cudaMalloc(&d_C, n * n * sizeof(int));
        cudaMemcpy(d_A, h_A, n * n * sizeof(int), cudaMemcpyHostToDevice);
        cudaMemcpy(d_B, h_B, n * n * sizeof(int), cudaMemcpyHostToDevice);

        for (int cfg = 0; cfg < num_configs; ++cfg) {
            dim3 threads(configs[cfg].tx, configs[cfg].ty);
            dim3 blocks((n + threads.x - 1) / threads.x,
                        (n + threads.y - 1) / threads.y);

            // прогреваем
            matmul_cuda<<<blocks, threads>>>(d_A, d_B, d_C, n);
            cudaDeviceSynchronize();

            double total_time = 0.0;
            for (int r = 0; r < repeats; ++r) {
                cudaEvent_t start, stop;
                cudaEventCreate(&start);
                cudaEventCreate(&stop);
                cudaEventRecord(start);
                matmul_cuda<<<blocks, threads>>>(d_A, d_B, d_C, n);
                cudaEventRecord(stop);
                
                cudaEventSynchronize(stop);

                float ms;
                cudaEventElapsedTime(&ms, start, stop);
                total_time += ms / 1000.0;
                
                cudaEventDestroy(start);
                cudaEventDestroy(stop);
            }
            double avg_time = total_time / repeats;

            ofstream out_csv(csv_filename, ios::app);
            out_csv << n << ";" << configs[cfg].name << ";" << fixed << setprecision(6) << avg_time << "\n";
            out_csv.close();

            cout << "  " << configs[cfg].name << " : " << avg_time << " sec\n";
        }

        delete[] h_A; delete[] h_B; delete[] h_C;
        cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    }

    cout << "Done. Results saved in " << csv_filename << endl;
    return 0;
}