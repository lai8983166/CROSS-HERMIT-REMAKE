
/* WARNING: Removing unreachable block (ram,0x0081e0a0) */
/* WARNING: Removing unreachable block (ram,0x0081e083) */
/* WARNING: Removing unreachable block (ram,0x0081e085) */
/* WARNING: Removing unreachable block (ram,0x0081e0a2) */

void FUN__text1__0081dff4(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c50)(param_1);
  local_c = (DAT_0086e380 ^ DAT_0086e384) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c00)(local_c);
  return;
}

