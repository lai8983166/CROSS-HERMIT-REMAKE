
/* WARNING: Removing unreachable block (ram,0x0081dc33) */
/* WARNING: Removing unreachable block (ram,0x0081dc35) */

void FUN__text1__0081dbff(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c78)(param_1);
  local_c = (DAT_0086e3a8 ^ DAT_0086e3ac) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c28)(local_c);
  return;
}

