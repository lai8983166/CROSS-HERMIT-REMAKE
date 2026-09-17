
undefined4 __fastcall FUN__text__004cd1e0(int param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [17];
  uint local_14;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = 0;
  for (uVar2 = 0; uVar2 < 5; uVar2 = uVar2 + 1) {
    if (((*(char *)(param_1 + 0x1cf + (uint)uVar2 * 0x12) != '\0') &&
        (bVar1 = *(byte *)(param_1 + 0x1d6 + (uint)uVar2 * 0x12), 1 < bVar1)) && (bVar1 < 7)) {
      local_14 = (uint)(ushort)((short)local_14 + 1);
    }
  }
  return CONCAT31((int3)(local_14 >> 8),local_14 == 0);
}

