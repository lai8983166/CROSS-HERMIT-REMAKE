
/* WARNING: Removing unreachable block (ram,0x00822be0) */
/* WARNING: Removing unreachable block (ram,0x00822bbf) */
/* WARNING: Removing unreachable block (ram,0x00822bc1) */
/* WARNING: Removing unreachable block (ram,0x00822be2) */

void FUN__text1__00822b8b(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c7c)(param_1);
  local_c = (DAT_0086e3ac ^ DAT_0086e3b0) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c2c)(local_c);
  return;
}

