
/* WARNING: Removing unreachable block (ram,0x0082261e) */
/* WARNING: Removing unreachable block (ram,0x00822620) */
/* WARNING: Removing unreachable block (ram,0x0082263a) */
/* WARNING: Removing unreachable block (ram,0x0082263c) */

void FUN__text1__008225ed(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c84)(param_1);
  local_c = (DAT_0086e3b4 ^ DAT_0086e3b8) << 1;
  if ((uVar1 & 0xffff0001) == 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c34)(local_c);
  return;
}

