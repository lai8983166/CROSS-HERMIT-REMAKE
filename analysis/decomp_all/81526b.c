
/* WARNING: Removing unreachable block (ram,0x0081529f) */
/* WARNING: Removing unreachable block (ram,0x008152a1) */
/* WARNING: Removing unreachable block (ram,0x008152d8) */
/* WARNING: Removing unreachable block (ram,0x008152da) */
/* WARNING: Removing unreachable block (ram,0x008152f4) */
/* WARNING: Removing unreachable block (ram,0x008152f6) */
/* WARNING: Removing unreachable block (ram,0x008152b6) */
/* WARNING: Removing unreachable block (ram,0x008152b8) */

void FUN__text1__0081526b(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c6c)(param_1);
  local_c = (DAT_0086e39c ^ DAT_0086e3a0) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c1c)(local_c);
  return;
}

