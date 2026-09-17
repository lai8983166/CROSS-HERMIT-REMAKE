
void FUN__text__004b9210(void)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [17];
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  for (uVar1 = 0; uVar1 < 100; uVar1 = uVar1 + 1) {
    *(undefined2 *)(&DAT_007a4aec + (uint)uVar1 * 2) = 0xffff;
  }
  DAT_007a4ae8 = 0;
  return;
}

