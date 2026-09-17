
/* WARNING: Removing unreachable block (ram,0x0081ea70) */
/* WARNING: Removing unreachable block (ram,0x0081ea72) */

void FUN__text1__0081ea3f(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c88)(param_1);
  local_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(local_c);
  return;
}

