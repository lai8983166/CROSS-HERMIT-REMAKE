
void FUN__text1__00820c7d(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c80)(param_1);
  local_c = (DAT_0086e3b0 ^ DAT_0086e3b4) << 1;
  if ((uVar1 & 0x80) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c30)(local_c);
  return;
}

