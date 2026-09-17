
/* WARNING: Removing unreachable block (ram,0x00820e74) */
/* WARNING: Removing unreachable block (ram,0x00820e76) */
/* WARNING: Removing unreachable block (ram,0x00820ec4) */
/* WARNING: Removing unreachable block (ram,0x00820ec6) */
/* WARNING: Removing unreachable block (ram,0x00820e9c) */
/* WARNING: Removing unreachable block (ram,0x00820e9e) */

void FUN__text1__00820e40(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c58)(param_1);
  local_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(local_c);
  return;
}

