
void FUN__text__004d33a0(short param_1)

{
  bool bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [17];
  short local_14;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  for (uVar2 = 0; uVar2 < 0x54; uVar2 = uVar2 + 1) {
    if ((&DAT_007e18a0)[(uint)uVar2 * 0xc + param_1 * 0x4a0] == '\x06') {
      bVar1 = true;
      for (local_14 = 0; local_14 < 8; local_14 = local_14 + 1) {
        if ((int)*(short *)(&DAT_007e183a + local_14 * 2 + param_1 * 0x4a0) == uVar2 + 1) {
          bVar1 = false;
        }
      }
      if (bVar1) {
        (&DAT_007e18a0)[(uint)uVar2 * 0xc + param_1 * 0x4a0] = 5;
      }
    }
  }
  return;
}

