
/* WARNING: Removing unreachable block (ram,0x00814f4e) */
/* WARNING: Removing unreachable block (ram,0x00814f50) */

void FUN__text1__00814f1a(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c5c)(param_1);
  local_c = (DAT_0086e38c ^ DAT_0086e390) << 1;
  if ((uVar1 & 4) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c0c)(local_c);
  return;
}

