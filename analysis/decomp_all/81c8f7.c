
/* WARNING: Removing unreachable block (ram,0x0081c9d9) */
/* WARNING: Removing unreachable block (ram,0x0081c9db) */
/* WARNING: Removing unreachable block (ram,0x0081c9ee) */
/* WARNING: Removing unreachable block (ram,0x0081c9f0) */

void FUN__text1__0081c8f7(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c80)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e3b0 ^ DAT_0086e3b4) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c30)(local_c);
  return;
}

