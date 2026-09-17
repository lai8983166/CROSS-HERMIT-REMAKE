
void FUN__text1__00820477(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c70)(param_1);
  local_c = (DAT_0086e3a0 ^ DAT_0086e3a4) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c20)(local_c);
  return;
}

