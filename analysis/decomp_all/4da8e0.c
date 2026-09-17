
void FUN__text__004da8e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  param_1 = param_1 * 0x2a;
  DAT_007f4488 = *(undefined2 *)(&DAT_006ad1d0 + param_1);
  DAT_007f448a = *(undefined2 *)(&DAT_006ad1d2 + param_1);
  DAT_007f448c._3_1_ = (&DAT_006ad1d4)[param_1];
  DAT_007f4490 = 0;
  DAT_007f4491 = 0;
  DAT_007f4492 = (ushort)(byte)(&DAT_006ad1d7)[param_1];
  DAT_007f4494 = (ushort)(byte)(&DAT_006ad1d8)[param_1];
  DAT_007f4496 = (ushort)(byte)(&DAT_006ad1d9)[param_1];
  DAT_007f4498 = (ushort)(byte)(&DAT_006ad1da)[param_1];
  DAT_007f449a = (ushort)(byte)(&DAT_006ad1db)[param_1];
  DAT_007f449c = (ushort)(byte)(&DAT_006ad1dc)[param_1];
  DAT_007f449e = (ushort)(byte)(&DAT_006ad1dd)[param_1];
  DAT_007f44a0 = (ushort)(byte)(&DAT_006ad1de)[param_1];
  DAT_007f44a2 = (&DAT_006ad1df)[param_1];
  DAT_007f44a3 = (&DAT_006ad1d5)[param_1];
  DAT_007f44a4 = (&DAT_006ad1d6)[param_1];
  if ((&DAT_006ad1e0)[param_1] == -1) {
    DAT_007f44a8 = 0x7fffffff;
  }
  else {
    DAT_007f44a8 = (uint)(byte)(&DAT_006ad1e0)[param_1] * 0xe10;
  }
  DAT_007f44ac = (uint)(byte)(&DAT_006ad1e1)[param_1] * 0xe10;
  DAT_007f44b0 = (uint)(byte)(&DAT_006ad1e2)[param_1] * 0xe10;
  DAT_007f44b4 = (uint)(byte)(&DAT_006ad1e3)[param_1] * 0xe10;
  DAT_007f44b8 = (&DAT_006ad1e4)[param_1];
  DAT_007f44b9 = (&DAT_006ad1e5)[param_1];
  DAT_007f44ba = (&DAT_006ad1e6)[param_1];
  DAT_007f44bb = (&DAT_006ad1e7)[param_1];
  DAT_007f44bc = (&DAT_006ad1e8)[param_1];
  DAT_007f44bd = (&DAT_006ad1e9)[param_1];
  for (local_10 = 0; local_10 != 0x10; local_10 = local_10 + 1) {
    (&DAT_007f44be)[local_10] = *(undefined *)((int)(&DAT_006ad1d0 + param_1) + local_10 + 0x1a);
  }
  DAT_007f448c._1_1_ = 0;
  DAT_007f448c._2_1_ = 0;
  DAT_007f448c._0_1_ = 0;
  return;
}

