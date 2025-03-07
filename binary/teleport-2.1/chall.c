#include <stdio.h>
#include <stdlib.h>

void useless() {
    asm("jmp *%rsp");
}

int main() {
    char destination[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to my Teleporter! Where would you like to go?");
    gets(destination);

    puts("\nSafe journey!!\n");
    return 0;
}