
/* WARNING: Removing unreachable block (ram,0x00818ed8) */
/* WARNING: Removing unreachable block (ram,0x00818eb7) */
/* WARNING: Removing unreachable block (ram,0x00818eb9) */
/* WARNING: Removing unreachable block (ram,0x00818eda) */

void FUN__text1__00818e83(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c78)(param_1);
  local_c = (DAT_0086e3a8 ^ DAT_0086e3ac) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c28)(local_c);
  return;
}

