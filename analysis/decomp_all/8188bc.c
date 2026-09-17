
/* WARNING: Removing unreachable block (ram,0x00818922) */
/* WARNING: Removing unreachable block (ram,0x00818924) */

void FUN__text1__008188bc(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c88)(param_1);
  local_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if ((uVar1 & 0x40) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(local_c);
  return;
}

