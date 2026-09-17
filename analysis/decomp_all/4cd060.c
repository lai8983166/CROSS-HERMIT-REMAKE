
undefined4 __fastcall FUN__text__004cd060(int param_1)

{
  ushort uVar1;
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
  for (uVar2 = 0; uVar2 < 10; uVar2 = uVar2 + 1) {
    if (((*(short *)(param_1 + 0x6f60 + (uint)uVar2 * 0xe0) != 0) &&
        (uVar1 = *(ushort *)(param_1 + 0x6f62 + (uint)uVar2 * 0xe0), 2 < uVar1)) && (uVar1 < 8)) {
      local_14 = (uint)(ushort)((short)local_14 + 1);
    }
  }
  return CONCAT31((int3)(local_14 >> 8),local_14 == 0);
}

