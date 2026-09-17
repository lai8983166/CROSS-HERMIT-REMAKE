
undefined4 FUN__text__004b5af0(int param_1,uint param_2)

{
  ushort *puVar1;
  bool bVar2;
  undefined2 uVar4;
  ushort *puVar3;
  int iVar5;
  ushort *puVar6;
  undefined4 *puVar7;
  bool bVar8;
  undefined4 local_68 [20];
  uint local_18;
  uint local_14;
  
  puVar7 = local_68;
  for (iVar5 = 0x19; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  puVar1 = (ushort *)(&DAT_007aacaa + (param_2 & 0xffff) * 2);
  iVar5 = (param_2 & 0xffff) * 0x38;
  local_14 = (uint)*(ushort *)(&DAT_006d511a + iVar5);
  local_18 = (uint)*(ushort *)(param_1 + 6);
  bVar8 = (&DAT_006e45f8)[local_14 + local_18 * 0xf] != '\0';
  bVar2 = (byte)(&DAT_006d5122)[iVar5] <= *(byte *)(param_1 + 0x50);
  puVar6 = (ushort *)((*puVar1 >> 8 & 0xf) - 1);
  uVar4 = (undefined2)((uint)puVar6 >> 0x10);
  puVar3 = puVar1;
  switch(puVar6) {
  case (ushort *)0x0:
    puVar3 = puVar6;
    if (!bVar2 || !bVar8) {
      puVar3 = (ushort *)(CONCAT22(uVar4,*puVar1) & 0xfffff0ff | 0x200);
      *puVar1 = (ushort)puVar3;
    }
    break;
  case (ushort *)0x1:
    puVar3 = (ushort *)0x0;
    if (bVar2 && bVar8) {
      *puVar1 = *puVar1 & 0xf0ff | 0x100;
      puVar3 = puVar1;
    }
    break;
  case (ushort *)0x2:
    puVar3 = puVar6;
    if (!bVar2 || !bVar8) {
      *puVar1 = *puVar1 & 0xf0ff | 0x400;
      puVar3 = puVar1;
    }
    break;
  case (ushort *)0x3:
    puVar3 = puVar6;
    if (bVar2 && bVar8) {
      puVar3 = (ushort *)(CONCAT22(uVar4,*puVar1) & 0xfffff0ff | 0x300);
      *puVar1 = (ushort)puVar3;
    }
  }
  return CONCAT22((short)((uint)puVar3 >> 0x10),1);
}

