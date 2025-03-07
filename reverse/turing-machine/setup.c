#include <stdint.h>
#include <stdio.h>
uint8_t setup(void)

{
  long in_FS_OFFSET;
  int local_50;
  int local_4c;
  short local_48 [28];
  long local_10;

  uint8_t tape[30] = {0};

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_48[0] = 0x1d;
  local_48[1] = 0x46;
  local_48[2] = 7;
  local_48[3] = 5;
  local_48[4] = 0x14;
  local_48[5] = 0;
  local_48[6] = 6;
  local_48[7] = 0x61;
  local_48[8] = 0x28;
  local_48[9] = 0;
  local_48[10] = 0x7a;
  local_48[11] = 10;
  local_48[12] = 0x36;
  local_48[13] = 0x39;
  local_48[14] = 0x74;
  local_48[15] = 0x1b;
  local_48[16] = 0;
  local_48[17] = 0x41;
  local_48[18] = 0x3c;
  local_48[19] = 7;
  local_48[20] = 0;
  local_48[21] = 0x20;
  local_48[22] = 0x5d;
  local_48[23] = 0x75;
  local_48[24] = 0x20;
  local_4c = 0xf;
  for (local_50 = 0; local_50 < 0x19; local_50 = local_50 + 1) {
    *(uint8_t *)(tape + (long)local_4c * 2) =
         *(uint8_t *)(tape + (long)local_4c * 2) ^ local_48[local_50];
    local_4c = local_4c + 2;
  }

  for(int i = 0; i < 30; i++) {
    printf("%d", tape);
  }
}

int main(int argc, char *argv[])
{
  setup();


  return 0;
}
