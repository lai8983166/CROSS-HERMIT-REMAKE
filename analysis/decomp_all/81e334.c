
/* WARNING: Removing unreachable block (ram,0x0081e370) */
/* WARNING: Removing unreachable block (ram,0x0081e372) */
/* WARNING: Removing unreachable block (ram,0x0081e38c) */
/* WARNING: Removing unreachable block (ram,0x0081e38e) */

void FUN__text1__0081e334(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c84)(param_1);
  local_c = (DAT_0086e3b4 ^ DAT_0086e3b8) << 1;
  if ((uVar1 & 0x41) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c34)(local_c);
  return;
}

