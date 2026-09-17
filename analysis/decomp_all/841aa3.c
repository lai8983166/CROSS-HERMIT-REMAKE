
void FUN__text1__00841aa3(int param_1)

{
  uint uVar1;
  uint uVar2;
  
  if (*(int *)(param_1 + 0x16b4) < 0xe) {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)(2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
  }
  uVar1 = (uint)DAT_00873842;
  if ((int)(0x10 - uVar1) < *(int *)(param_1 + 0x16b4)) {
    uVar2 = (uint)DAT_00873840;
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         DAT_00873840 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar1;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         DAT_00873840 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
    *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar1;
  }
  FUN__text1__0084493d(param_1);
  if ((*(int *)(param_1 + 0x16ac) + 0xb) - *(int *)(param_1 + 0x16b4) < 9) {
    if (*(int *)(param_1 + 0x16b4) < 0xe) {
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) |
           (ushort)(2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
      *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
    }
    else {
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) |
           (ushort)(2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)*(undefined2 *)(param_1 + 0x16b0);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(short *)(param_1 + 0x16b0) =
           (short)(2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
      *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
    }
    uVar1 = (uint)DAT_00873842;
    if ((int)(0x10 - uVar1) < *(int *)(param_1 + 0x16b4)) {
      uVar2 = (uint)DAT_00873840;
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) |
           DAT_00873840 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)*(undefined2 *)(param_1 + 0x16b0);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(short *)(param_1 + 0x16b0) =
           (short)((int)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
      *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar1;
    }
    else {
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) |
           DAT_00873840 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
      *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar1;
    }
    FUN__text1__0084493d(param_1);
  }
  *(undefined4 *)(param_1 + 0x16ac) = 7;
  return;
}

