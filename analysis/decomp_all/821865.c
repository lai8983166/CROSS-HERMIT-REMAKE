
/* WARNING: Removing unreachable block (ram,0x00821910) */
/* WARNING: Removing unreachable block (ram,0x008218e3) */
/* WARNING: Removing unreachable block (ram,0x008218e5) */
/* WARNING: Removing unreachable block (ram,0x00821912) */

void FUN__text1__00821865(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c8c)(param_1);
  local_c = (DAT_0086e3bc ^ DAT_0086e3c0) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c3c)(local_c);
  return;
}

