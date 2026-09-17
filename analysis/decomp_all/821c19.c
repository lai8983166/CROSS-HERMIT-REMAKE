
/* WARNING: Removing unreachable block (ram,0x00821cb1) */
/* WARNING: Removing unreachable block (ram,0x00821cb3) */

void FUN__text1__00821c19(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c64)(param_1);
  local_c = (DAT_0086e394 ^ DAT_0086e398) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c14)(local_c);
  return;
}

