#define _GNU_SOURCE
#include <stdio.h>

long ptrace(int request, int pid, int addr, int data) {
      printf("Calling fake ptrace\n");
      return 0;
}
