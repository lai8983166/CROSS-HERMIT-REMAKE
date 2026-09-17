
void FUN__text1__00817788(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c98)(param_1);
  local_c = (DAT_0086e3c8 ^ DAT_0086e3cc) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c48)(local_c);
  return;
}

