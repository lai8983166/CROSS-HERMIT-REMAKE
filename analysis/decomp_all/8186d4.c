
void FUN__text1__008186d4(undefined4 param_1)

{
  uint uVar1;
  uint local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c78)(param_1);
  local_c = (DAT_0086e3a8 ^ DAT_0086e3ac) << 1;
  if (((uVar1 & 0x80) == 0) != ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c28)(local_c);
  return;
}

