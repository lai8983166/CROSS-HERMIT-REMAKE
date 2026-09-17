
void FUN__text__004cd2a0(void)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  uint local_14;
  uint local_10;
  undefined1 local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
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
  local_8 = 0x4cd340;
  FUN__text__0056ce80();
  return;
}

