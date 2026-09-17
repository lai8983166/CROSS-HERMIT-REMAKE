
void FUN__text1__00844a26(int param_1)

{
  if (*(int *)(param_1 + 0x16b4) < 9) {
    if (0 < *(int *)(param_1 + 0x16b4)) {
      *(undefined1 *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           *(undefined1 *)(param_1 + 0x16b0);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    }
  }
  else {
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  }
  *(undefined2 *)(param_1 + 0x16b0) = 0;
  *(undefined4 *)(param_1 + 0x16b4) = 0;
  return;
}

