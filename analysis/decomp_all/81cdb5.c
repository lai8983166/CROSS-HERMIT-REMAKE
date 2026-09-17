
/* WARNING: Removing unreachable block (ram,0x0081ce99) */
/* WARNING: Removing unreachable block (ram,0x0081ce9b) */

void FUN__text1__0081cdb5(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  undefined4 local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c84)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e3b4 ^ DAT_0086e3b8) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c34)(local_c);
  return;
}

