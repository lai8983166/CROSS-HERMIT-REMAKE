
void FUN__text1__00820db3(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c64)(param_1);
  local_c = (DAT_0086e394 ^ DAT_0086e398) << 1;
  if ((uVar1 & 0x40) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c14)(local_c);
  return;
}

