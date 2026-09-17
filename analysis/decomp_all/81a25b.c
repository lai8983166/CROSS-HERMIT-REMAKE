
/* WARNING: Removing unreachable block (ram,0x0081a302) */
/* WARNING: Removing unreachable block (ram,0x0081a2d5) */
/* WARNING: Removing unreachable block (ram,0x0081a2d7) */
/* WARNING: Removing unreachable block (ram,0x0081a304) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__0081a25b(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c9c)(param_1);
  local_c = (DAT_0086e3cc ^ _DAT_0086e3d0) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c4c)(local_c);
  return;
}

