
/* WARNING: Removing unreachable block (ram,0x00815607) */
/* WARNING: Removing unreachable block (ram,0x00815609) */
/* WARNING: Removing unreachable block (ram,0x0081561c) */
/* WARNING: Removing unreachable block (ram,0x0081561e) */

void FUN__text1__008155d3(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c94)(param_1);
  local_c = (DAT_0086e3c4 ^ DAT_0086e3c8) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c44)(local_c);
  return;
}

