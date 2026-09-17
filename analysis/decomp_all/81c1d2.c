
/* WARNING: Removing unreachable block (ram,0x0081c22a) */
/* WARNING: Removing unreachable block (ram,0x0081c209) */
/* WARNING: Removing unreachable block (ram,0x0081c20b) */
/* WARNING: Removing unreachable block (ram,0x0081c22c) */

void FUN__text1__0081c1d2(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c90)(param_1);
  local_c = (DAT_0086e3c0 ^ DAT_0086e3c4) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c40)(local_c);
  return;
}

