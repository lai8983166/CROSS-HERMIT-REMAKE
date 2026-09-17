
void FUN__text__004d3d00(void)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_50 [19];
  
  puVar4 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  for (uVar1 = 0; uVar1 < 5; uVar1 = uVar1 + 1) {
    for (uVar3 = 0; uVar3 < 4; uVar3 = uVar3 + 1) {
      *(undefined2 *)(&DAT_007aaae0 + (uint)uVar1 * 8 + (uint)uVar3 * 2) = 0xffff;
      *(undefined2 *)(&DAT_007aaab8 + (uint)uVar1 * 8 + (uint)uVar3 * 2) = 0xffff;
    }
    *(undefined2 *)(&DAT_007aaaae + (uint)uVar1 * 2) = 0xffff;
    *(undefined2 *)(&DAT_007aaaa4 + (uint)uVar1 * 2) = 0xffff;
  }
  for (uVar1 = 0; uVar1 < 0xf0; uVar1 = uVar1 + 1) {
    (&DAT_007a5120)[uVar1] = 0;
  }
  for (uVar1 = 0; uVar1 < 0x28; uVar1 = uVar1 + 1) {
    *(undefined2 *)(&DAT_007a5210 + (uint)uVar1 * 2) = 0;
  }
  DAT_007a5260 = 0;
  for (uVar1 = 0; uVar1 < 0x14; uVar1 = uVar1 + 1) {
    *(undefined2 *)(&DAT_007a5262 + (uint)uVar1 * 2) = 0;
  }
  DAT_007a528a = 0;
  return;
}

