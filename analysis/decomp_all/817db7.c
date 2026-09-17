
/* WARNING: Removing unreachable block (ram,0x00817deb) */
/* WARNING: Removing unreachable block (ram,0x00817ded) */
/* WARNING: Removing unreachable block (ram,0x00817e31) */
/* WARNING: Removing unreachable block (ram,0x00817e33) */

void FUN__text1__00817db7(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c68)(param_1);
  local_c = (DAT_0086e398 ^ DAT_0086e39c) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c18)(local_c);
  return;
}

