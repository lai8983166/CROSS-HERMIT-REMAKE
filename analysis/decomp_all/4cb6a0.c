
undefined4 __fastcall FUN__text__004cb6a0(int param_1)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [18];
  uint local_10;
  uint local_c;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = (uint)*(ushort *)(param_1 + 0x16);
  local_c = 0;
  while (local_c < local_10) {
    uVar1 = *(ushort *)(param_1 + 0x18 + local_c * 0x110);
    if ((1 < uVar1) && (uVar1 < 4)) {
      *(undefined2 *)(param_1 + 0x18 + local_c * 0x110) = 1;
    }
    local_c = (uint)(ushort)((short)local_c + 1);
  }
  return CONCAT31((int3)(local_c >> 8),1);
}

