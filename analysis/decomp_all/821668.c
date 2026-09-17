
void FUN__text1__00821668(undefined4 param_1)

{
  uint uVar1;
  undefined4 uStack_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c94)(param_1);
  uStack_c = (DAT_0086e3c4 ^ DAT_0086e3c8) << 1;
  if ((uVar1 & 0x41) != 0) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c44)(uStack_c);
  return;
}

