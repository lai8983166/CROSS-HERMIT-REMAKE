
/* WARNING: Removing unreachable block (ram,0x0081d8db) */
/* WARNING: Removing unreachable block (ram,0x0081d8dd) */
/* WARNING: Removing unreachable block (ram,0x0081d91a) */
/* WARNING: Removing unreachable block (ram,0x0081d91c) */

void FUN__text1__0081d8a7(undefined4 param_1)

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

