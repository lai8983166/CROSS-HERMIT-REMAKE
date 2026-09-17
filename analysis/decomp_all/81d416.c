
void FUN__text1__0081d416(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c54)(param_1);
  local_c = (DAT_0086e384 ^ DAT_0086e388) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c04)(local_c);
  return;
}

