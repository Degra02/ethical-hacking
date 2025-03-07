
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>

// Define the original strlen function pointer
typedef size_t (*orig_strlen_type)(const char *str);

// Override the strlen function
size_t strlen(const char *str) {
    // Print a message to indicate that the function has been called
    printf("Custom strlen called!\n");
    // Return 0x21 (33 in decimal)
    return 0x21;
}
