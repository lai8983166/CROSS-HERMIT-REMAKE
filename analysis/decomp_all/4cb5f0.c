
ushort __fastcall FUN__text__004cb5f0(int param_1)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  ushort uVar4;
  undefined4 *puVar5;
  undefined4 local_58 [21];
  
  puVar5 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  uVar4 = 0;
  for (uVar3 = 0; uVar3 < *(ushort *)(param_1 + 0x16); uVar3 = uVar3 + 1) {
    uVar1 = *(ushort *)(param_1 + 0x18 + (uint)uVar3 * 0x110);
    if ((1 < uVar1) && (uVar1 < 5)) {
      uVar4 = uVar4 + 1;
    }
  }
  if (uVar4 == 0) {
    uVar4 = 1;
  }
  else {
    uVar4 = uVar4 & 0xff00;
  }
  return uVar4;
}

