
int __thiscall FUN__text1__00842c85(undefined4 param_1,int param_2)

{
  int iVar1;
  
  FUN__text1__00842d3c(param_2,param_2 + 0x8c,*(undefined4 *)(param_2 + 0xb14),param_1);
  FUN__text1__00842d3c(param_2,param_2 + 0x980,*(undefined4 *)(param_2 + 0xb20));
  FUN__text1__0084234e(param_2,param_2 + 0xb28);
  iVar1 = 0x12;
  while ((2 < iVar1 && (*(short *)(param_2 + 0xa76 + (uint)(byte)(&DAT_0087342c)[iVar1] * 4) == 0)))
  {
    iVar1 = iVar1 + -1;
  }
  *(int *)(param_2 + 0x16a0) = *(int *)(param_2 + 0x16a0) + 0xe + (iVar1 + 1) * 3;
  return iVar1;
}

