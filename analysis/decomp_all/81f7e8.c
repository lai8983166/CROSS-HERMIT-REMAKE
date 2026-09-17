
/* WARNING: Removing unreachable block (ram,0x0081f84c) */
/* WARNING: Removing unreachable block (ram,0x0081f84a) */
/* WARNING: Removing unreachable block (ram,0x0081f871) */
/* WARNING: Removing unreachable block (ram,0x0081f873) */
/* WARNING: Removing unreachable block (ram,0x0081f87e) */
/* WARNING: Removing unreachable block (ram,0x0081f880) */

void FUN__text1__0081f7e8(undefined4 param_1)

{
  ulonglong uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c5c)(param_1);
  local_c = (DAT_0086e38c ^ DAT_0086e390) << 1;
  if ((uVar1 & 0xffff0001) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c0c)(local_c,(int)(uVar1 >> 0x20));
  return;
}

