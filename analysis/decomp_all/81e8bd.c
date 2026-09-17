
/* WARNING: Removing unreachable block (ram,0x0081e923) */
/* WARNING: Removing unreachable block (ram,0x0081e925) */

void FUN__text1__0081e8bd(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c50)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e380 ^ DAT_0086e384) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c00)(local_c);
  return;
}

