
/* WARNING: Removing unreachable block (ram,0x0081e2c5) */
/* WARNING: Removing unreachable block (ram,0x0081e2c7) */

void FUN__text1__0081e25f(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c5c)(param_1);
  local_c = (DAT_0086e38c ^ DAT_0086e390) << 1;
  if ((uVar1 & 0x40) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c0c)(local_c);
  return;
}

