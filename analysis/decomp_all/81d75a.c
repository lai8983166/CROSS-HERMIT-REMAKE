
void FUN__text1__0081d75a(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c94)(param_1);
  local_c = (DAT_0086e3c4 ^ DAT_0086e3c8) << 1;
  if ((uVar1 & 0x41) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c44)(local_c);
  return;
}

