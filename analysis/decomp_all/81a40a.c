
void FUN__text1__0081a40a(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c68)(param_1);
  local_c = (DAT_0086e398 ^ DAT_0086e39c) << 1;
  if ((uVar1 & 0x80) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c18)(local_c);
  return;
}

