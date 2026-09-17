
/* WARNING: Removing unreachable block (ram,0x00817cad) */
/* WARNING: Removing unreachable block (ram,0x00817caf) */

void FUN__text1__00817be8(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c84)(param_1);
  local_c = (DAT_0086e3b4 ^ DAT_0086e3b8) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c34)(local_c);
  return;
}

