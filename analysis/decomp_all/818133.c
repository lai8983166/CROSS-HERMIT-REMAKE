
/* WARNING: Removing unreachable block (ram,0x00818164) */
/* WARNING: Removing unreachable block (ram,0x00818166) */

void FUN__text1__00818133(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c84)(param_1);
  local_c = (DAT_0086e3b4 ^ DAT_0086e3b8) << 1;
  if ((uVar1 & 0x800) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c34)(local_c);
  return;
}

