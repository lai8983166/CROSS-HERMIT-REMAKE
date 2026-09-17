
bool FUN__text1__00843ed4(int param_1,int param_2,int param_3)

{
  byte bVar1;
  uint local_8;
  
  *(undefined2 *)(*(int *)(param_1 + 0x169c) + *(int *)(param_1 + 0x1698) * 2) = (undefined2)param_2
  ;
  *(undefined1 *)(*(int *)(param_1 + 0x1690) + *(int *)(param_1 + 0x1698)) = (undefined1)param_3;
  *(int *)(param_1 + 0x1698) = *(int *)(param_1 + 0x1698) + 1;
  if (param_2 == 0) {
    *(short *)(param_1 + 0x8c + param_3 * 4) = *(short *)(param_1 + 0x8c + param_3 * 4) + 1;
  }
  else {
    *(int *)(param_1 + 0x16a8) = *(int *)(param_1 + 0x16a8) + 1;
    *(short *)(param_1 + 0x490 + (uint)(byte)(&DAT_00873b38)[param_3] * 4) =
         *(short *)(param_1 + 0x490 + (uint)(byte)(&DAT_00873b38)[param_3] * 4) + 1;
    if (param_2 - 1U < 0x100) {
      bVar1 = (&DAT_00873937)[param_2];
    }
    else {
      bVar1 = (&DAT_00873a38)[param_2 - 1U >> 7];
    }
    local_8 = (uint)bVar1;
    *(short *)(param_1 + 0x980 + local_8 * 4) = *(short *)(param_1 + 0x980 + local_8 * 4) + 1;
  }
  return *(int *)(param_1 + 0x1698) == *(int *)(param_1 + 0x1694) + -1;
}

