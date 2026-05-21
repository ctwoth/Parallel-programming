#pragma once

int to_int(char* num) {
    int rez = 0;
    bool is_neg = false;
    if (*num == '-') { is_neg = true; ++num; }

    while (*num != 0) {
        rez = rez * 10 + *num - '0';
        num++;
    }
    if (is_neg) rez = -rez;
    return rez;
}

char* read_file(FILE* file) {
    char* rez;
    size_t size;
    fseek(file, 0, SEEK_END);
    size = ftell(file);
    fseek(file, 0, SEEK_SET);

    rez = new char[size + 1];
    fread_s(rez, size + 1, sizeof(char), size, file);
    rez[size] = 0;

    return rez;
}