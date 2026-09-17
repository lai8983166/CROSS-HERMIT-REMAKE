
/* WARNING: Removing unreachable block (ram,0x008156ff) */
/* WARNING: Removing unreachable block (ram,0x00815701) */
/* WARNING: Removing unreachable block (ram,0x008156d5) */
/* WARNING: Removing unreachable block (ram,0x008156d7) */

void FUN__text1__00815688(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c50)(param_1);
  local_c = (DAT_0086e380 ^ DAT_0086e384) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c00)(local_c);
  return;
}

