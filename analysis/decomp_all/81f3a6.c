
void FUN__text1__0081f3a6(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c7c)(param_1);
  local_c = (DAT_0086e3ac ^ DAT_0086e3b0) << 1;
  if (((uVar1 & 0x80) == 0) == ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c2c)(local_c);
  return;
}

