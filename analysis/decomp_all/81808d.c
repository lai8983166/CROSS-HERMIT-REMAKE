
void FUN__text1__0081808d(undefined4 param_1)

{
  uint uVar1;
  undefined4 uStack_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c78)(param_1);
  uStack_c = (DAT_0086e3a8 ^ DAT_0086e3ac) << 1;
  if ((uVar1 & 0x40) != 0) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c28)(uStack_c);
  return;
}

