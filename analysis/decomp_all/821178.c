
/* WARNING: Removing unreachable block (ram,0x0082123b) */
/* WARNING: Removing unreachable block (ram,0x0082123d) */

void FUN__text1__00821178(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c94)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x88) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e3c4 ^ DAT_0086e3c8) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c44)(local_c);
  return;
}

