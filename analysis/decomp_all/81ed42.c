
/* WARNING: Removing unreachable block (ram,0x0081ed73) */
/* WARNING: Removing unreachable block (ram,0x0081ed75) */
/* WARNING: Removing unreachable block (ram,0x0081ed88) */
/* WARNING: Removing unreachable block (ram,0x0081ed8a) */

void FUN__text1__0081ed42(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c80)(param_1);
  local_c = (DAT_0086e3b0 ^ DAT_0086e3b4) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c30)(local_c);
  return;
}

