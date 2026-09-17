
/* WARNING: Removing unreachable block (ram,0x0081e199) */
/* WARNING: Removing unreachable block (ram,0x0081e17c) */
/* WARNING: Removing unreachable block (ram,0x0081e17e) */
/* WARNING: Removing unreachable block (ram,0x0081e19b) */

void FUN__text1__0081e0e1(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c60)(param_1);
  local_c = (DAT_0086e390 ^ DAT_0086e394) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c10)(local_c);
  return;
}

