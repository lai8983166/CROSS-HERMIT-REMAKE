
void FUN__text1__008202af(undefined4 param_1)

{
  uint uVar1;
  undefined4 uStack_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c8c)(param_1);
  uStack_c = (DAT_0086e3bc ^ DAT_0086e3c0) << 1;
  if ((uVar1 & 0x40) == 0) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c3c)(uStack_c);
  return;
}

