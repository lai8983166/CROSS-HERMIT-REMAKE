
void FUN__text__004cd350(void)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  uint local_28;
  undefined1 local_24 [4];
  uint local_20;
  uint local_14;
  uint local_10;
  undefined1 local_c;
  undefined4 local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  local_14 = local_14 & 0xffff0000;
  local_10 = local_10 & 0xffff0000;
  while ((local_10 & 0xffff) < 10) {
    cVar1 = FUN__text__004cb5f0();
    if (cVar1 != '\x01') {
      local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
    }
    local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
  }
  if ((local_14 & 0xffff) == 0) {
    local_c = 1;
  }
  FUN__text__004d5ec0(local_24,0,0,0x400,0x300);
  local_28 = CONCAT31(local_28._1_3_,1);
  if ((local_20 & 1) != 0) {
    local_28 = (uint)local_28._1_3_ << 8;
  }
  iVar2 = FUN__text__004128f0(0x39,0);
  if (iVar2 != 0) {
    local_28 = local_28 & 0xffffff00;
  }
  if ((local_28 & 0xff) == 0) {
    local_10 = local_10 & 0xffff0000;
    while ((local_10 & 0xffff) < 10) {
      FUN__text__004cb6a0();
      local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
    }
    if (DAT_007a49fc != 0) {
      FUN__text__0041e500();
    }
    local_c = 1;
  }
  local_8 = 0x4cd4c8;
  FUN__text__0056ce80();
  return;
}

