
/* WARNING: Removing unreachable block (ram,0x008217ed) */
/* WARNING: Removing unreachable block (ram,0x008217ef) */

void FUN__text1__0082170c(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  undefined4 local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c70)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e3a0 ^ DAT_0086e3a4) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c20)(local_c);
  return;
}

