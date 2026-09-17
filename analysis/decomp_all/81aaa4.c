
void FUN__text1__0081aaa4(undefined4 param_1)

{
  undefined4 uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c58)(param_1);
  local_c = (DAT_0086e388 ^ DAT_0086e38c) << 1;
  if ((CONCAT22((short)((uint)uVar1 >> 0x10),(ushort)(byte)uVar1) & 0xffff0001) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c08)(local_c);
  return;
}

