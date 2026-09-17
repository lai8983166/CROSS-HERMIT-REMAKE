
void FUN__text__00497d10(void)

{
  int iVar1;
  short sVar2;
  short sVar3;
  undefined4 *puVar4;
  undefined4 local_54 [18];
  short local_c;
  short local_8;
  
  puVar4 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = *(short *)(DAT_007a49f4 + 0x2a49e) + 0x200;
  local_c = *(short *)(DAT_007a49f4 + 0x2a4a0) + 0x11d;
  sVar2 = *(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 4) << 5;
  sVar3 = *(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 6) << 4;
  if (sVar2 <= local_8) {
    local_8 = sVar2;
  }
  if (sVar3 <= local_c) {
    local_c = sVar3;
  }
  *(short *)(DAT_007a49f8 + 0x24c0) = local_8;
  *(short *)(DAT_007a49f8 + 0x24c2) = local_c;
  return;
}

