#include<stdio.h>
#include<random>


void gen_matrix(FILE* f, int dim, int min, int len) {
	for (int i = 0; i < dim; ++i) {
		for (int j = 0; j < dim; ++j) {
			fprintf_s(f, "%d ", rand() % len + min);
		}
		fseek(f, -1, SEEK_CUR);
		fprintf_s(f, "\n");
	}
}


int main() {
	int dim, min, max;
	char file_path[128];
	FILE* f;

	printf_s("enter matrix dimension: ");
	scanf_s("%d", &dim);
	printf_s("enter min num: ");
	scanf_s("%d", &min);
	printf_s("enter max num: ");
	scanf_s("%d", &max);
	printf_s("enter save path: ");
	scanf_s("%s", file_path, 128);

	fopen_s(&f, file_path, "w+");
	srand(time(NULL));

	gen_matrix(f, dim, min, (max - min) + 1);

	return 0;
}