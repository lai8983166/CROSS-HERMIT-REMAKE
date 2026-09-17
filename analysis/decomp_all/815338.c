
/* WARNING: Removing unreachable block (ram,0x0081538d) */
/* WARNING: Removing unreachable block (ram,0x0081536c) */
/* WARNING: Removing unreachable block (ram,0x0081536e) */
/* WARNING: Removing unreachable block (ram,0x0081538f) */

void FUN__text1__00815338(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c8c)(param_1);
  local_c = (DAT_0086e3bc ^ DAT_0086e3c0) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c3c)(local_c);
  return;
}

