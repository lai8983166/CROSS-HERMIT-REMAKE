
void __thiscall FUN__text__004cd8d0(int param_1,short param_2)

{
  bool bVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_50 [19];
  
  puVar4 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (param_2 == 1) {
    bVar1 = false;
    while (!bVar1) {
      *(undefined1 *)(param_1 + 5) = 0;
      bVar1 = true;
    }
  }
  else {
    bVar1 = false;
    while (!bVar1) {
      *(undefined1 *)(param_1 + 5) = 0;
      bVar1 = true;
    }
    for (uVar3 = 0; uVar3 < 5; uVar3 = uVar3 + 1) {
      *(undefined1 *)(param_1 + 0x1cf + (uint)uVar3 * 0x12) = 0;
      *(undefined2 *)(param_1 + 0x1dc + (uint)uVar3 * 0x12) = 0xffff;
      *(undefined2 *)(param_1 + 0x1de + (uint)uVar3 * 0x12) = 0xffff;
    }
    for (uVar3 = 0; uVar3 < 10; uVar3 = uVar3 + 1) {
      *(undefined2 *)(param_1 + 0x6f60 + (uint)uVar3 * 0xe0) = 0;
      *(undefined2 *)(param_1 + 0x6f94 + (uint)uVar3 * 0xe0) = 0xffff;
      *(undefined2 *)(param_1 + 0x6f96 + (uint)uVar3 * 0xe0) = 0xffff;
      *(undefined2 *)(param_1 + 0x6f62 + (uint)uVar3 * 0xe0) = 0;
      *(undefined2 *)(param_1 + 0x6f82 + (uint)uVar3 * 0xe0) = 0;
    }
    for (uVar3 = 0; uVar3 < 0x38; uVar3 = uVar3 + 1) {
      *(undefined1 *)(param_1 + 0x92a0 + (uint)uVar3) = 0;
    }
    for (uVar3 = 0; uVar3 < 0x38; uVar3 = uVar3 + 1) {
      *(undefined2 *)(param_1 + 0x446 + (uint)uVar3 * 0xab8) = 0;
    }
    for (uVar3 = 0; uVar3 < 10; uVar3 = uVar3 + 1) {
      *(undefined2 *)(param_1 + 0x6f60 + (uint)uVar3 * 0xe0) = 0;
      *(undefined2 *)(param_1 + 0x6f62 + (uint)uVar3 * 0xe0) = 0;
      *(undefined2 *)(param_1 + 0x6f82 + (uint)uVar3 * 0xe0) = 0;
    }
    for (uVar3 = 0; uVar3 < 0x14; uVar3 = uVar3 + 1) {
      *(undefined1 *)(param_1 + 0x228 + (uint)uVar3 * 0x1a) = 0;
    }
    *(undefined2 *)(param_1 + 0x9248) = 0;
  }
  return;
}

