
/* WARNING: Removing unreachable block (ram,0x00820770) */
/* WARNING: Removing unreachable block (ram,0x00820772) */

void FUN__text1__0082070a(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c6c)(param_1);
  local_c = (DAT_0086e39c ^ DAT_0086e3a0) << 1;
  if ((uVar1 & 0x41) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c1c)(local_c);
  return;
}

