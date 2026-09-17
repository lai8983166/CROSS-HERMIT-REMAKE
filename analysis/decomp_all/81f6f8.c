
/* WARNING: Removing unreachable block (ram,0x0081f754) */
/* WARNING: Removing unreachable block (ram,0x0081f73b) */
/* WARNING: Removing unreachable block (ram,0x0081f73d) */
/* WARNING: Removing unreachable block (ram,0x0081f756) */

void FUN__text1__0081f6f8(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c64)(param_1);
  local_c = (DAT_0086e394 ^ DAT_0086e398) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c14)(local_c);
  return;
}

