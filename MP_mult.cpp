#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>

using namespace std;
using namespace chrono;

typedef vector<vector<int>> Matrix;


Matrix generate_matrix(size_t dim) {
    Matrix matr(dim, vector<int>(dim));
    
    for (size_t i = 0; i < dim; ++i)
        for (size_t j = 0; j < dim; ++j)
            matr[i][j] = rand() % 11; //0-10

    return matr;
}


Matrix multiply_parallel(const Matrix& matr1, const Matrix& matr2, int num_threads) {
    size_t dim = matr1.size();
    Matrix rez(dim, vector<int>(dim, 0));

    omp_set_num_threads(num_threads);

#pragma omp parallel for schedule(static)
    for (int i = 0; i < (int)dim; ++i) {
        for (size_t j = 0; j < dim; ++j) {
            int sum = 0;
            for (size_t k = 0; k < dim; ++k) {
                sum += matr1[i][k] * matr2[k][j];
            }
            rez[i][j] = sum;
        }
    }
    return rez;
}

double measure_time(const Matrix& a, const Matrix& b, int num_threads, int repeats) {
    double total_time = 0.0;
    for (int r = 0; r < repeats; ++r) {
        auto start = steady_clock::now();
        Matrix rez = multiply_parallel(a, b, num_threads);
        auto end = steady_clock::now();

        total_time += duration<double>(end - start).count();
    }
    return total_time / repeats;
}

// Append result to CSV file
void save_result(const string& filename, size_t size, int threads, double time_sec) {
    ofstream out(filename, ios::app);
    out << size << "," << threads << "," << fixed << setprecision(6) << time_sec << "\n";
    out.close();
}

int main() {
    srand(time(NULL));

    vector<size_t> sizes = { 200, 400, 800, 1200, 1600, 2000 };
    vector<int> thread_counts = { 1, 2, 4, 8, 12, 16 };
    int repeats_per_test = 3;
    string output_file = "results.csv";

    // Create CSV header
    ofstream out(output_file);
    out << "size,threads,time_sec\n";
    out.close();

    cout << "Starting...\n";

    for (size_t size : sizes) {
        cout << "Matrix size: " << size << " x " << size << endl;

        // Generate two matrices once per size
        Matrix A = generate_matrix(size);
        Matrix B = generate_matrix(size);

        for (int threads : thread_counts) {
            double avg_time = measure_time(A, B, threads, repeats_per_test);
            cout << "  Threads: " << threads << " -> average time: " << avg_time << " sec" << endl;
            save_result(output_file, size, threads, avg_time);
        }
        cout << endl;
    }

    cout << "End. Results saved in " << output_file << endl;
    return 0;
}