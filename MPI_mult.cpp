#include <iostream>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <mpi.h>

using namespace std;

typedef vector<vector<int> > Matrix;

void fillRandom(Matrix& mat) {
    int n = mat.size();
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            mat[i][j] = rand() % 11;
}

void multiply_mpi(const Matrix& A, const Matrix& B, int rank, int size, int n) {
    vector<int> B_flat(n * n);
    if (rank == 0) {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                B_flat[i * n + j] = B[i][j];
    }
    MPI_Bcast(B_flat.data(), n * n, MPI_INT, 0, MPI_COMM_WORLD);

    int rows_per_proc = n / size;
    int remainder = n % size;
    int local_rows = rows_per_proc + (rank < remainder ? 1 : 0);

    vector<int> sendcounts(size), displs(size);
    int offset = 0;
    for (int p = 0; p < size; ++p) {
        sendcounts[p] = (p < remainder) ? rows_per_proc + 1 : rows_per_proc;
        displs[p] = offset;
        offset += sendcounts[p];
    }

    vector<int> A_flat;
    if (rank == 0) {
        A_flat.resize(n * n);
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                A_flat[i * n + j] = A[i][j];
    }

    vector<int> A_local_flat(local_rows * n);
    MPI_Scatterv(A_flat.data(), sendcounts.data(), displs.data(), MPI_INT,
        A_local_flat.data(), local_rows * n, MPI_INT,
        0, MPI_COMM_WORLD);

    // Преобразуем в 2D для удобства
    Matrix A_local(local_rows, vector<int>(n));
    for (int i = 0; i < local_rows; ++i)
        for (int j = 0; j < n; ++j)
            A_local[i][j] = A_local_flat[i * n + j];

    Matrix B_mat(n, vector<int>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            B_mat[i][j] = B_flat[i * n + j];

    // Локальное умножение i-k-j
    Matrix C_local(local_rows, vector<int>(n, 0));
    for (int i = 0; i < local_rows; ++i) {
        for (int k = 0; k < n; ++k) {
            int aik = A_local[i][k];
            for (int j = 0; j < n; ++j) {
                C_local[i][j] += aik * B_mat[k][j];
            }
        }
    }

    // Упаковка результата и отправка на 0 (без сбора, т.к. результат не нужен)
    vector<int> C_local_flat(local_rows * n);
    for (int i = 0; i < local_rows; ++i)
        for (int j = 0; j < n; ++j)
            C_local_flat[i * n + j] = C_local[i][j];

    vector<int> recvcounts_elem(size), displs_elem(size);
    for (int p = 0; p < size; ++p) {
        recvcounts_elem[p] = sendcounts[p] * n;
        displs_elem[p] = displs[p] * n;
    }

    vector<int> C_flat;
    if (rank == 0) C_flat.resize(n * n);
    MPI_Gatherv(C_local_flat.data(), local_rows * n, MPI_INT,
        C_flat.data(), recvcounts_elem.data(), displs_elem.data(), MPI_INT,
        0, MPI_COMM_WORLD);
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    srand(time(NULL) + rank);

    const int sizes[] = { 200, 400, 800, 1200, 1600, 2000 };
    const int num_sizes = 6;
    const int repeats = 3;
    
    for (int idx = 0; idx < num_sizes; ++idx) {
        int n = sizes[idx];
        if (rank == 0)
            cout << "Size: " << n << " x " << n << endl;

        // Только на процессе 0 генерируем матрицы
        Matrix A, B;
        if (rank == 0) {
            A.resize(n, vector<int>(n));
            B.resize(n, vector<int>(n));
            fillRandom(A);
            fillRandom(B);
        }

        double total_time = 0.0;
        for (int r = 0; r < repeats; ++r) {
            MPI_Barrier(MPI_COMM_WORLD);
            double start = MPI_Wtime();
            multiply_mpi(A, B, rank, size, n);
            MPI_Barrier(MPI_COMM_WORLD);
            double end = MPI_Wtime();
            total_time += (end - start);
        }
        double avg_time = total_time / repeats;

        if (rank == 0) {
            cout << "  Average time: " << avg_time << " sec\n";
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }

    if (rank == 0)
        cout << "\nDone." << endl;

    MPI_Finalize();
    return 0;
}