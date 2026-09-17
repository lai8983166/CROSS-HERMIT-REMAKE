
/* WARNING: Removing unreachable block (ram,0x0081512b) */
/* WARNING: Removing unreachable block (ram,0x0081512d) */
/* WARNING: Removing unreachable block (ram,0x00815145) */
/* WARNING: Removing unreachable block (ram,0x00815147) */

void FUN__text1__008150fa(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c70)(param_1);
  local_c = (DAT_0086e3a0 ^ DAT_0086e3a4) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c20)(local_c);
  return;
}

