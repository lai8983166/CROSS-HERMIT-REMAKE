
/* WARNING: Removing unreachable block (ram,0x0081db4c) */
/* WARNING: Removing unreachable block (ram,0x0081db4e) */
/* WARNING: Removing unreachable block (ram,0x0081db61) */
/* WARNING: Removing unreachable block (ram,0x0081db63) */

void FUN__text1__0081da72(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c68)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e398 ^ DAT_0086e39c) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c18)(local_c);
  return;
}

