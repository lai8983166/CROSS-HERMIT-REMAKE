
/* WARNING: Removing unreachable block (ram,0x008193b8) */
/* WARNING: Removing unreachable block (ram,0x008193ba) */

void FUN__text1__0081936e(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c90)(param_1);
  local_c = (DAT_0086e3c0 ^ DAT_0086e3c4) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c40)(local_c);
  return;
}

