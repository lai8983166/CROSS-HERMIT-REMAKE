
void FUN__text1__0081c14c(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c54)(param_1);
  local_c = (DAT_0086e384 ^ DAT_0086e388) << 1;
  if ((uVar1 & 0x40) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c04)(local_c);
  return;
}

