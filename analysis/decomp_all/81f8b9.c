
/* WARNING: Removing unreachable block (ram,0x0081f8ed) */
/* WARNING: Removing unreachable block (ram,0x0081f8ef) */

void FUN__text1__0081f8b9(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c58)(param_1);
  local_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(local_c);
  return;
}

