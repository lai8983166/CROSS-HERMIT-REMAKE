
void FUN__text1__0081d36d(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c50)(param_1);
  local_c = (DAT_0086e380 ^ DAT_0086e384) << 1;
  if ((uVar1 & 0x40) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c00)(local_c);
  return;
}

