
/* WARNING: Removing unreachable block (ram,0x0082036e) */
/* WARNING: Removing unreachable block (ram,0x00820370) */

void FUN__text1__00820346(undefined4 param_1)

{
  undefined4 uVar1;
  ushort uVar2;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c74)(param_1);
  uVar2 = (ushort)((uint)uVar1 >> 0x10);
  local_c = (DAT_0086e3a4 ^ DAT_0086e3a8) << 1;
  if ((CONCAT22(uVar2 & 0xff | (ushort)(((uint)(uVar2 >> 8) << 0x18) >> 0x10),(ushort)(byte)uVar1) &
      0xffffff01) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c24)(local_c);
  return;
}

