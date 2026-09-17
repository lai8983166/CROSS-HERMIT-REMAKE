
/* WARNING: Removing unreachable block (ram,0x00822a5c) */
/* WARNING: Removing unreachable block (ram,0x00822a5e) */
/* WARNING: Removing unreachable block (ram,0x00822a6c) */
/* WARNING: Removing unreachable block (ram,0x00822a6e) */

void FUN__text1__00822a1e(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c74)(param_1);
  local_c = (DAT_0086e3a4 ^ DAT_0086e3a8) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c24)(local_c);
  return;
}

