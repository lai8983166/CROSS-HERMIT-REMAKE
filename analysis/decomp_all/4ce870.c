
void FUN__text__004ce870(void)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__004d0860();
  do {
    uVar1 = FUN__text__004ce8f0();
    local_c = CONCAT31(local_c._1_3_,uVar1);
    FUN__text__00422360(0);
  } while ((local_c & 0xff) != 0);
  FUN__text__004d0750();
  local_8 = 0x4ce8df;
  FUN__text__0056ce80();
  return;
}

