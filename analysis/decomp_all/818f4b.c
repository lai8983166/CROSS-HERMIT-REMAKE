
/* WARNING: Removing unreachable block (ram,0x00818fb1) */
/* WARNING: Removing unreachable block (ram,0x00818fb3) */

void FUN__text1__00818f4b(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c58)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(local_c);
  return;
}

