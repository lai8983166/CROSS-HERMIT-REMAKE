
/* WARNING: Removing unreachable block (ram,0x00819cc7) */
/* WARNING: Removing unreachable block (ram,0x00819cc9) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__00819c96(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c9c)(param_1);
  local_c = (DAT_0086e3cc ^ _DAT_0086e3d0) << 1;
  if ((uVar1 & 0xffff0001) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c4c)(local_c);
  return;
}

