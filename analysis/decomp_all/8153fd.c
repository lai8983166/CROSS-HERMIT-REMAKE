
/* WARNING: Removing unreachable block (ram,0x0081542e) */
/* WARNING: Removing unreachable block (ram,0x00815430) */
/* WARNING: Removing unreachable block (ram,0x0081544f) */
/* WARNING: Removing unreachable block (ram,0x00815451) */
/* WARNING: Removing unreachable block (ram,0x0081546c) */
/* WARNING: Removing unreachable block (ram,0x0081546e) */

void FUN__text1__008153fd(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c70)(param_1);
  local_c = (DAT_0086e3a0 ^ DAT_0086e3a4) << 1;
  if ((uVar1 & 0xffff0001) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c20)(local_c);
  return;
}

