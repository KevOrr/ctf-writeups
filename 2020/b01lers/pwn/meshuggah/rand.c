#include <stdlib.h>
#include <stdio.h>

const char* USAGE = "rand <SEED> <COUNT>\n";

int main(int argc, char **argv) {
    if (argc != 3) {
        fputs(USAGE, stderr);
        exit(1);
    }

    int seed = atoi(argv[1]);
    int n = atoi(argv[2]);

    srand(seed);
    for (int i=0; i<n; i++)
        printf("%d\n", rand());
}
