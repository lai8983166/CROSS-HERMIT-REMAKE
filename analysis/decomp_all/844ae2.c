
void FUN__text1__00844ae2(int param_1,undefined1 *param_2,int param_3,int param_4)

{
  byte bVar1;
  
  FUN__text1__00844a26(param_1);
  *(undefined4 *)(param_1 + 0x16ac) = 8;
  if (param_4 != 0) {
    *(byte *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) = (byte)param_3;
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    bVar1 = (byte)((uint)param_3 >> 8);
    *(byte *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) = bVar1;
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(byte *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) = ~(byte)param_3;
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(byte *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) = ~bVar1;
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  }
  while (param_3 != 0) {
    *(undefined1 *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) = *param_2;
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    param_2 = param_2 + 1;
    param_3 = param_3 + -1;
  }
  return;
}

