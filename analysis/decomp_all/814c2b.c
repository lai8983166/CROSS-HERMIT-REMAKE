
void FUN__text1__00814c2b(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c58)(param_1);
  local_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if (((uVar1 & 0x80) == 0) == ((uVar1 & 0x800) == 0)) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(local_c);
  return;
}

