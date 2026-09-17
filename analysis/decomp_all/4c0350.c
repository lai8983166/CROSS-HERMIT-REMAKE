
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004c0350(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined2 local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = _DAT_007a52f8;
  local_10 = FUN__text__004d1ba0((int)_DAT_007a52f8,0,0x14);
  for (local_14 = 0; local_14 < local_10; local_14 = local_14 + 1) {
    local_18 = *(undefined2 *)(&DAT_007a52d0 + local_14 * 2 + local_c * 0x70);
    FUN__text__004c0c10(CONCAT22((short)((uint)(local_c * 0x70) >> 0x10),local_18));
  }
  local_8 = 0x4c03ef;
  FUN__text__0056ce80();
  return;
}

