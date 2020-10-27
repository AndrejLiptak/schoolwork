#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printEncode(uint32_t num)
{
    uint8_t array[5] = { 0 };

    for (int i = 4; i >= 0; i--) {
        *(array + i) = (num % 85) + 33;
        num /= 85;
    }
    for (int i = 0; i <= 4; i++)
        putchar(*(array + i));
}

int encode(void)
{
    int16_t chr;
    int8_t bytes_count = 0;
    uint32_t num = 0;

    while ((chr = getchar()) != EOF) {
        if (bytes_count == 4) {
            printEncode(num);
            num = 0;
            bytes_count = 0;
        }
        bytes_count++;
        num = num << 8;
        num = num | chr;
    }
    if (bytes_count != 0) {
        num = num << 8 * (4 - bytes_count);
        printEncode(num);
    }
    printf("\n");
    return 0;
}

void decode_print(uint32_t num)
{
    uint8_t array[4] = { 0 };

    for (int i = 3; i >= 0; i--) {
        *(array + i) = num & 0xff;
        num >>= 8;
    }
    for (int i = 0; i < 4; i++)
        putchar(*(array + i));
}

int decode(void)
{
    int16_t chr = 0;
    uint32_t num = 0;
    int8_t byteCount = 0;

    while ((chr = getchar()) != EOF) {
        if (isspace(chr))
            continue;
        if (chr > 117 || chr < 33)
            return 1;
        num *= 85;
        num += (chr - 33);
        byteCount++;
        if (byteCount == 5) {
            decode_print(num);
            byteCount = 0;
            num = 0;
        }
    }
    if (byteCount != 0)
        return 1;
    return 0;
}

// ================================
// DO NOT MODIFY THE FOLLOWING CODE
// ================================
int main(int argc, char *argv[])
{
    int retcode = 1;
    if (argc == 1 || (argc == 2 && strcmp(argv[1], "-e") == 0)) {
        retcode = encode();
    } else if (argc == 2 && strcmp(argv[1], "-d") == 0) {
        retcode = decode();
    } else {
        fprintf(stderr, "usage: %s [-e|-d]\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (retcode != 0) {
        fprintf(stderr, "an error occured\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
