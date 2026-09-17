
/* WARNING: Removing unreachable block (ram,0x0081d83e) */
/* WARNING: Removing unreachable block (ram,0x0081d840) */

void FUN__text1__0081d80a(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c64)(param_1);
  local_c = (DAT_0086e394 ^ DAT_0086e398) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c14)(local_c);
  return;
}

