
void FUN__text1__00842ed9(int param_1,int param_2,int param_3,int param_4)

{
  ushort uVar1;
  int local_8;
  
  if (*(int *)(param_1 + 0x16b4) < 0xc) {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_2 + -0x101 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 5;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_2 - 0x101U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)(param_2 - 0x101U & 0xffff) >>
                (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xb;
  }
  if (*(int *)(param_1 + 0x16b4) < 0xc) {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_3 + -1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 5;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_3 - 1U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)(param_3 - 1U & 0xffff) >>
                (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xb;
  }
  if (*(int *)(param_1 + 0x16b4) < 0xd) {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_4 + -4 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 4;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         (ushort)(param_4 - 4U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)(param_4 - 4U & 0xffff) >>
                (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xc;
  }
  for (local_8 = 0; local_8 < param_4; local_8 = local_8 + 1) {
    if (*(int *)(param_1 + 0x16b4) < 0xe) {
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) |
           *(short *)(param_1 + 0xa76 + (uint)(byte)(&DAT_0087342c)[local_8] * 4) <<
           ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
      *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
    }
    else {
      uVar1 = *(ushort *)(param_1 + 0xa76 + (uint)(byte)(&DAT_0087342c)[local_8] * 4);
      *(ushort *)(param_1 + 0x16b0) =
           *(ushort *)(param_1 + 0x16b0) | uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f)
      ;
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)*(undefined2 *)(param_1 + 0x16b0);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
           (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
      *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
      *(short *)(param_1 + 0x16b0) =
           (short)((int)(uint)uVar1 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
      *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
    }
  }
  FUN__text1__008433fc(param_1,param_1 + 0x8c,param_2 + -1);
  FUN__text1__008433fc(param_1,param_1 + 0x980,param_3 + -1);
  return;
}

