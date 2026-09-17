
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004a1c70(void)

{
  short sVar1;
  bool bVar2;
  ushort uVar3;
  ushort uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_5c [16];
  short local_1c;
  
  puVar6 = local_5c;
  for (iVar5 = 0x16; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  bVar2 = false;
  for (uVar3 = 0; uVar3 < 3; uVar3 = uVar3 + 1) {
    *(undefined2 *)(&DAT_007d62fa + (uint)uVar3 * 2) = 0;
  }
  for (uVar3 = 0; (int)(uint)uVar3 < (int)DAT_007a5b62; uVar3 = uVar3 + 1) {
    uVar4 = (ushort)(byte)(&DAT_007a5667)[(uint)uVar3 * 0x10];
    if ((&DAT_007a5668)[(uint)uVar3 * 0x10] == '\0') {
      sVar1 = *(short *)(&DAT_007d62fa + (short)uVar4 * 2);
      *(short *)(&DAT_007d62fa + (short)uVar4 * 2) =
           *(short *)(&DAT_007d62fa + (short)uVar4 * 2) + 1;
      *(ushort *)(&DAT_007d599a + sVar1 * 10 + (short)uVar4 * 800) =
           (ushort)(byte)(&DAT_007a5665)[(uint)uVar3 * 0x10];
      *(ushort *)(&DAT_007d599c + sVar1 * 10 + (short)uVar4 * 800) =
           (ushort)(byte)(&DAT_007a5666)[(uint)uVar3 * 0x10];
      *(undefined2 *)(&DAT_007d599e + sVar1 * 10 + (short)uVar4 * 800) =
           *(undefined2 *)(&DAT_007a5662 + (uint)uVar3 * 0x10);
      *(ushort *)(&DAT_007d59a2 + sVar1 * 10 + (short)uVar4 * 800) = uVar3;
      if (*(short *)(&DAT_007a566a + (uint)uVar3 * 0x10) < 1) {
        *(undefined2 *)(&DAT_007d59a0 + sVar1 * 10 + (short)uVar4 * 800) =
             *(undefined2 *)(&DAT_007a566a + (uint)uVar3 * 0x10);
      }
      else {
        *(short *)(&DAT_007d59a0 + sVar1 * 10 + (short)uVar4 * 800) =
             *(short *)(&DAT_007a566a + (uint)uVar3 * 0x10) -
             *(short *)(&DAT_007a5670 + (uint)uVar3 * 0x10);
      }
      if ((uVar4 == 0) && (DAT_007a55fa = 1, !bVar2)) {
        bVar2 = true;
        DAT_007aab0a = 1;
        _DAT_007aab0c = 0;
        _DAT_007aab0e = 0;
        DAT_007aab10 = *(undefined2 *)(&DAT_007d599a + sVar1 * 10);
        DAT_007aab12 = *(undefined2 *)(&DAT_007d599c + sVar1 * 10);
        DAT_007aab16 = *(undefined2 *)(&DAT_007d599e + sVar1 * 10);
        DAT_007aab18 = 0;
        DAT_007aab14 = sVar1;
      }
    }
  }
  for (uVar3 = 0; uVar3 < 3; uVar3 = uVar3 + 1) {
    *(undefined2 *)(&DAT_007d6300 + (uint)uVar3 * 2) = 0;
    local_1c = (short)((*(ushort *)(&DAT_007d62fa + (uint)uVar3 * 2) + 1) / 2);
    if (local_1c < 5) {
      local_1c = 0;
    }
    else {
      local_1c = local_1c + -4;
    }
    *(short *)(&DAT_007d6306 + (uint)uVar3 * 2) = local_1c;
  }
  if (DAT_007d62fe == 0) {
    DAT_007d5984 = 1;
  }
  return;
}

