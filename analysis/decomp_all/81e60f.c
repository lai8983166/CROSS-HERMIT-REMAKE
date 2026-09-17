
/* WARNING: Removing unreachable block (ram,0x0081e707) */
/* WARNING: Removing unreachable block (ram,0x0081e70e) */
/* WARNING: Removing unreachable block (ram,0x0081e736) */
/* WARNING: Removing unreachable block (ram,0x0081e738) */
/* WARNING: Removing unreachable block (ram,0x0081e76e) */
/* WARNING: Removing unreachable block (ram,0x0081e770) */

void FUN__text1__0081e60f(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  undefined4 local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c6c)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  local_c = (DAT_0086e39c ^ DAT_0086e3a0) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c1c)(local_c);
  return;
}

