
/* WARNING: Removing unreachable block (ram,0x0081bcb2) */
/* WARNING: Removing unreachable block (ram,0x0081bcb4) */

void FUN__text1__0081bbaa(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  undefined4 uStack_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c58)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  uStack_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if (bVar1) {
    uStack_c = uStack_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(uStack_c);
  return;
}

