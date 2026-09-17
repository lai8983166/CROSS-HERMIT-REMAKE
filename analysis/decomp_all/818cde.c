
/* WARNING: Removing unreachable block (ram,0x00818dca) */
/* WARNING: Removing unreachable block (ram,0x00818dd1) */
/* WARNING: Removing unreachable block (ram,0x00818df9) */
/* WARNING: Removing unreachable block (ram,0x00818dfb) */
/* WARNING: Removing unreachable block (ram,0x00818e31) */
/* WARNING: Removing unreachable block (ram,0x00818e33) */

void FUN__text1__00818cde(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  undefined4 local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c60)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e390 ^ DAT_0086e394) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c10)(local_c);
  return;
}

