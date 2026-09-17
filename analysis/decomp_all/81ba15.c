
/* WARNING: Removing unreachable block (ram,0x0081baf7) */
/* WARNING: Removing unreachable block (ram,0x0081baf9) */
/* WARNING: Removing unreachable block (ram,0x0081bb0c) */
/* WARNING: Removing unreachable block (ram,0x0081bb0e) */

void FUN__text1__0081ba15(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c98)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e3c8 ^ DAT_0086e3cc) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c48)(local_c);
  return;
}

