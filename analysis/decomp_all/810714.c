
void __thiscall FUN__text1__00810714(int param_1,uint param_2,char param_3)

{
  undefined4 local_8;
  
  for (local_8 = 1 << (param_3 - 1U & 0x1f); local_8 != 0; local_8 = local_8 >> 1) {
    if ((param_2 & local_8) != 0) {
      **(byte **)(param_1 + 0xc) = **(byte **)(param_1 + 0xc) | *(byte *)(param_1 + 0x14);
    }
    *(byte *)(param_1 + 0x14) = *(byte *)(param_1 + 0x14) >> 1;
    if (*(char *)(param_1 + 0x14) == '\0') {
      *(int *)(param_1 + 0xc) = *(int *)(param_1 + 0xc) + 1;
      if (*(uint *)(param_1 + 0xc) < *(uint *)(param_1 + 0x10)) {
        **(undefined1 **)(param_1 + 0xc) = 0;
      }
      else {
        *(undefined1 *)(param_1 + 0x15) = 1;
      }
      *(undefined1 *)(param_1 + 0x14) = 0x80;
    }
  }
  return;
}

