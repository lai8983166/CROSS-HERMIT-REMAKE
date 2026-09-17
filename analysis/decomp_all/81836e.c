
/* WARNING: Removing unreachable block (ram,0x008183a2) */
/* WARNING: Removing unreachable block (ram,0x008183a4) */
/* WARNING: Removing unreachable block (ram,0x008183b9) */
/* WARNING: Removing unreachable block (ram,0x008183bb) */

void FUN__text1__0081836e(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c70)(param_1);
  local_c = (DAT_0086e3a0 ^ DAT_0086e3a4) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c20)(local_c);
  return;
}

