
/* WARNING: Removing unreachable block (ram,0x0081febf) */
/* WARNING: Removing unreachable block (ram,0x0081fec1) */
/* WARNING: Removing unreachable block (ram,0x0081fe74) */
/* WARNING: Removing unreachable block (ram,0x0081fe63) */
/* WARNING: Removing unreachable block (ram,0x0081fe65) */
/* WARNING: Removing unreachable block (ram,0x0081fe72) */
/* WARNING: Removing unreachable block (ram,0x0081fef2) */
/* WARNING: Removing unreachable block (ram,0x0081fef4) */
/* WARNING: Removing unreachable block (ram,0x0081ff02) */
/* WARNING: Removing unreachable block (ram,0x0081ff04) */

void FUN__text1__0081fdcd(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c88)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x88) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e3b8 ^ DAT_0086e3bc) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c38)(local_c);
  return;
}

