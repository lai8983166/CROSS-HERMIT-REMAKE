
/* WARNING: Removing unreachable block (ram,0x00815a94) */
/* WARNING: Removing unreachable block (ram,0x00815a96) */

void FUN__text1__00815a06(undefined4 param_1)

{
  ushort uVar1;
  undefined4 uVar2;
  uint local_c;
  
  uVar2 = (*(code *)PTR_DAT_00872c7c)(param_1);
  uVar1 = (ushort)((uint)uVar2 >> 0x10);
  local_c = (DAT_0086e3ac ^ DAT_0086e3b0) << 1;
  if ((CONCAT22(uVar1 & 0xff | (ushort)(((uint)(uVar1 >> 8) << 0x18) >> 0x10),(ushort)(byte)uVar2) &
      0xffffff01) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c2c)(local_c);
  return;
}

