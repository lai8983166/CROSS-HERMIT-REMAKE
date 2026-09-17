
/* WARNING: Removing unreachable block (ram,0x00819625) */
/* WARNING: Removing unreachable block (ram,0x00819627) */
/* WARNING: Removing unreachable block (ram,0x00819663) */
/* WARNING: Removing unreachable block (ram,0x00819665) */

void FUN__text1__008195f2(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c88)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(local_c);
  return;
}

