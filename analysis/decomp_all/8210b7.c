
/* WARNING: Removing unreachable block (ram,0x008210e9) */
/* WARNING: Removing unreachable block (ram,0x008210eb) */
/* WARNING: Removing unreachable block (ram,0x0082110d) */
/* WARNING: Removing unreachable block (ram,0x0082110f) */

void FUN__text1__008210b7(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c74)(param_1);
  local_c = (DAT_0086e3a4 ^ DAT_0086e3a8) << 1;
  if ((uVar1 & 4) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c24)(local_c);
  return;
}

