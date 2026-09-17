
void FUN__text1__0082194c(undefined4 param_1)

{
  uint uVar1;
  undefined4 uStack_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c88)(param_1);
  uStack_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if ((uVar1 & 0x41) == 0) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(uStack_c);
  return;
}

