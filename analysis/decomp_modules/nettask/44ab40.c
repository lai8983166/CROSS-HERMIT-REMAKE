
void FUN__text__0044ab40(void)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__0044abe0();
  local_c = (int)(uVar2 + ((int)uVar2 >> 0x1f & 3U)) >> 2;
  uVar2 = uVar2 & 0x80000003;
  if ((int)uVar2 < 0) {
    uVar2 = (uVar2 - 1 | 0xfffffffc) + 1;
  }
  if (uVar2 != 0) {
    local_c = local_c + 1;
  }
  uVar1 = local_c;
  local_10 = local_c;
  if ((int)local_c < 5) {
    if ((int)local_c < 2) {
      local_c = 1;
    }
  }
  else {
    local_c = 5;
  }
  FUN__text__00428220(uVar1 & 0xffff,CONCAT22((short)(uVar2 >> 0x10),(undefined2)local_c));
  local_8 = 0x44abda;
  FUN__text__0056ce80();
  return;
}

