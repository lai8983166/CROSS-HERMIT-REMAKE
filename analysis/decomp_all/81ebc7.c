
/* WARNING: Removing unreachable block (ram,0x0081ec28) */
/* WARNING: Removing unreachable block (ram,0x0081ec2a) */

void FUN__text1__0081ebc7(undefined4 param_1)

{
  bool bVar1;
  uint uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c64)(param_1);
  if (((uVar2 & 0x40) == 0) && (((uVar2 & 0x80) == 0) == ((uVar2 & 0x800) == 0))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  local_c = (DAT_0086e394 ^ DAT_0086e398) << 1;
  if (bVar1) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c14)(local_c);
  return;
}

