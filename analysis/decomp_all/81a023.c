
/* WARNING: Removing unreachable block (ram,0x0081a081) */
/* WARNING: Removing unreachable block (ram,0x0081a083) */

void FUN__text1__0081a023(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c8c)(param_1);
  local_c = (DAT_0086e3bc ^ DAT_0086e3c0) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c3c)(local_c);
  return;
}

