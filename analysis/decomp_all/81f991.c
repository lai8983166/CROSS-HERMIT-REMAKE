
/* WARNING: Removing unreachable block (ram,0x0081f9c5) */
/* WARNING: Removing unreachable block (ram,0x0081f9c7) */
/* WARNING: Removing unreachable block (ram,0x0081f9db) */
/* WARNING: Removing unreachable block (ram,0x0081f9dd) */

void FUN__text1__0081f991(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c60)(param_1);
  local_c = (DAT_0086e390 ^ DAT_0086e394) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c10)(local_c);
  return;
}

