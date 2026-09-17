
void FUN__text1__00841964(int param_1,undefined4 param_2,undefined4 param_3,uint param_4)

{
  if (*(int *)(param_1 + 0x16b4) < 0xe) {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_4 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_4 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)(param_4 & 0xffff) >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f)
                );
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
  }
  FUN__text1__00844ae2(param_1,param_2,param_3,1);
  return;
}

