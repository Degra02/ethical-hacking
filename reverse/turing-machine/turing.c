#include <stdint.h>
#include <stdio.h>

#define TAPE_SIZE 67
#define MARKED_VALUE 0xffff

void process_tape(uint16_t *tape) {
    int head = 0;
    int state = 0;
    uint8_t reg = 0;

    while (head < TAPE_SIZE && head >= 0) {
        switch (state) {
            case 0:
                if (tape[head] < 0) {
                    head++;
                } else {
                    reg = (uint8_t)tape[head];
                    tape[head] = MARKED_VALUE;
                    state = 1;
                    head++;
                }
                break;
            case 1:
                reg ^= (uint8_t)tape[head];
                tape[head] = MARKED_VALUE;
                state = 2;
                head--;
                break;
            case 2:
                if (tape[head] == -1) {
                    head--;
                } else {
                    state = 3;
                    head++;
                }
                break;
            case 3:
                tape[head] = (uint16_t)reg;
                state = 0;
                head++;
                break;
        }
    }
}

int main(int argc, char *argv[])
{
  uint16_t tape[TAPE_SIZE] = {0};
  process_tape(tape);

  for(int i = 0; i < TAPE_SIZE; i++) {
    printf("%d", tape[i]);
  }
  printf("\n");

  return 0;
}
