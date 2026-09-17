
/* WARNING: Removing unreachable block (ram,0x0081cd46) */
/* WARNING: Removing unreachable block (ram,0x0081cd48) */

void FUN__text1__0081cd15(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c74)(param_1);
  local_c = (DAT_0086e3a4 ^ DAT_0086e3a8) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c24)(local_c);
  return;
}

