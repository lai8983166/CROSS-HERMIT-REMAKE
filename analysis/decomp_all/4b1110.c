
uint __thiscall FUN__text__004b1110(int param_1,int param_2,uint param_3,uint param_4)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_88 [17];
  ushort auStack_44 [20];
  undefined *local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_88;
  for (iVar2 = 0x21; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  local_14 = CONCAT22(local_14._2_2_,*(undefined2 *)(&DAT_006d511a + (param_4 & 0xffff) * 0x38));
  local_18 = CONCAT22(local_18._2_2_,(short)*(char *)(param_1 + 0x570));
  local_1c = &DAT_006e45f8;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 0x14) {
    auStack_44[local_c & 0xffff] = 0;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_c = local_c & 0xffff0000;
  while( true ) {
    if ((local_18 & 0xffff) <= (local_c & 0xffff)) {
      return (uint)(auStack_44[local_14 & 0xffff] < (ushort)(byte)local_1c[local_14 & 0xffff]);
    }
    uVar1 = *(ushort *)(param_2 + 0x62 + (local_c & 0xffff) * 2);
    local_10 = CONCAT22(local_10._2_2_,uVar1);
    if (((uVar1 != 0) &&
        (auStack_44[*(ushort *)(&DAT_006d511a + (uint)uVar1 * 0x38)] =
              auStack_44[*(ushort *)(&DAT_006d511a + (uint)uVar1 * 0x38)] + 1,
        (param_3 & 0xffff) == (local_c & 0xffff))) &&
       (iVar2 = (local_10 & 0xffff) * 0x38,
       (uint)*(ushort *)(&DAT_006d511a + iVar2) == (local_14 & 0xffff))) break;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  return CONCAT22((short)((uint)iVar2 >> 0x10),1);
}

