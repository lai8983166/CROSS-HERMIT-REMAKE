
/* WARNING: Removing unreachable block (ram,0x0081b9d4) */
/* WARNING: Removing unreachable block (ram,0x0081b9b7) */
/* WARNING: Removing unreachable block (ram,0x0081b9b9) */
/* WARNING: Removing unreachable block (ram,0x0081b9d6) */

void FUN__text1__0081b921(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c80)(param_1);
  local_c = (DAT_0086e3b0 ^ DAT_0086e3b4) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c30)(local_c);
  return;
}

