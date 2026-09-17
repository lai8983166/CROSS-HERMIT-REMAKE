
undefined4 __fastcall FUN__text__004cdf80(int param_1)

{
  ushort uVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_4c [18];
  
  uVar2 = 0xcccccccc;
  puVar5 = local_4c;
  for (iVar4 = 0x12; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  uVar1 = 0;
  while (uVar1 < 10) {
    *(undefined2 *)(param_1 + 0x6f60 + (uint)uVar1 * 0xe0) = 0;
    *(undefined2 *)(param_1 + 0x6f62 + (uint)uVar1 * 0xe0) = 0;
    uVar3 = (uint)uVar1;
    *(undefined2 *)(param_1 + 0x6f82 + (int)((longlong)(int)uVar3 * 0xe0)) = 0;
    uVar1 = uVar1 + 1;
    uVar2 = CONCAT22((short)((ulonglong)((longlong)(int)uVar3 * 0xe0) >> 0x10),uVar1);
  }
  *(undefined1 *)(param_1 + 0x92e0) = 0;
  return CONCAT31((int3)((uint)uVar2 >> 8),1);
}

