
void FUN__text1__0081863f(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c68)(param_1);
  local_c = (DAT_0086e398 ^ DAT_0086e39c) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c18)(local_c);
  return;
}

