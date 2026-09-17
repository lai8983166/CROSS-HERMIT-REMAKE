
/* WARNING: Removing unreachable block (ram,0x008182d4) */
/* WARNING: Removing unreachable block (ram,0x008182bb) */
/* WARNING: Removing unreachable block (ram,0x008182bd) */
/* WARNING: Removing unreachable block (ram,0x008182d6) */

void FUN__text1__0081827c(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c88)(param_1);
  local_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if ((uVar1 & 0x800) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(local_c);
  return;
}

