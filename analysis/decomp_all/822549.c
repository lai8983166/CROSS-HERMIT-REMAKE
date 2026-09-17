
void FUN__text1__00822549(undefined4 param_1)

{
  uint uVar1;
  undefined4 uStack_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c50)(param_1);
  uStack_c = (DAT_0086e380 ^ DAT_0086e384) << 1;
  if ((uVar1 & 0x40) != 0) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c00)(uStack_c);
  return;
}

