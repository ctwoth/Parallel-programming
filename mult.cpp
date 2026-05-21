#include<stdio.h>
#include<vector>
#include<string.h>
#include<chrono>
#include"base.h"

using namespace std;

typedef vector<vector<int>> Matrix;


Matrix read_matrix(const char* path) {
    Matrix matr;
    FILE* f;
    char* text;
    char* line, * line_ctx = NULL;
    char* num, * num_ctx = NULL;

    fopen_s(&f, path, "rb");
    if (!f) return matr;

    text = read_file(f);
    fclose(f);

    line = strtok_s(text, "\r\n", &line_ctx);
    while (line) {
        num = strtok_s(line, " ", &num_ctx);
        matr.push_back(vector<int>());
        while (num) {
            matr[matr.size() - 1].push_back(to_int(num));
            num = strtok_s(NULL, " ", &num_ctx);
        }
        line = strtok_s(NULL, "\r\n", &line_ctx);
    }
    delete[] text;

    return matr;
}

void load_matrix(Matrix& matr, const char* path) {
    FILE* f;

    fopen_s(&f, path, "w+");

    if (!f) return;

    size_t dim = matr.size();
    for (size_t i = 0; i < dim; ++i) {
        for (size_t j = 0; j < dim; ++j) {
            fprintf_s(f, "%d ", matr[i][j]);
        }
        fseek(f, -1, SEEK_CUR);
        fprintf_s(f, "\n");
    }
}

Matrix multiply(Matrix& matr1, Matrix& matr2) {
    Matrix rez;
    size_t dim = matr1.size();

    for (size_t i = 0; i < dim; ++i) {
        rez.push_back(vector<int>());

        for (size_t j = 0; j < dim; ++j) {
            rez[i].push_back(0);
            for (size_t k = 0; k < dim; ++k) {
                rez[i][j] += matr1[i][k] * matr2[k][j];
            }
        }
    }

    return rez;
}

void print_matrix(Matrix& matrix) {
    for (size_t i = 0; i < matrix.size(); ++i) {
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            printf("%ld ", matrix[i][j]);
        }
        printf("\n");
    }
}


int main() {
    char path1[128], path2[128];
    printf("Entire path to matrix 1: ");
    scanf_s("%s", path1, 128);

    printf("Entire path to matrix 2: ");
    scanf_s("%s", path2, 128);

    auto start = chrono::steady_clock::now();

    Matrix matr1 = read_matrix(path1);
    Matrix matr2 = read_matrix(path2);

    auto end = chrono::steady_clock::now();

    printf("\nReading time: %lf seconds\n\n", chrono::duration<double>(end - start).count());


    start = chrono::steady_clock::now();

    Matrix rez = multiply(matr1, matr2);

    end = chrono::steady_clock::now();


    getchar(); // '\n' rest in buffer

    printf("Print result matrix? [type 'y' for yes]: ");

    if (getchar() == 'y') {
        printf("\nResult:\n");
        print_matrix(rez);
        printf("\n");
    }
    printf("\Multiplying time: %lf miliseconds\n\n", chrono::duration<double>(end - start).count());

    getchar(); // '\n' rest in buffer
    printf("Save result matrix? [type 'y' for yes]: ");

    if (getchar() == 'y') {
        printf("\nEntire result path: ");
        scanf_s("%s", path1, 128);
        load_matrix(rez, path1);
    }

    return 0;
}
