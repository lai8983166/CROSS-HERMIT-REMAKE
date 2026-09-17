
/* WARNING: Removing unreachable block (ram,0x0082223f) */
/* WARNING: Removing unreachable block (ram,0x00822241) */
/* WARNING: Removing unreachable block (ram,0x00822264) */
/* WARNING: Removing unreachable block (ram,0x00822266) */

void FUN__text1__00822167(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c78)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x88) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e3a8 ^ DAT_0086e3ac) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c28)(local_c);
  return;
}

