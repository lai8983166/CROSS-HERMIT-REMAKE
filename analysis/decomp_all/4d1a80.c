
void FUN__text__004d1a80(void)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  uint local_10;
  undefined4 local_c;
  int *local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  FUN__text__004d0860();
  do {
    uVar1 = FUN__text__004ce8f0();
    local_10 = CONCAT31(local_10._1_3_,uVar1);
    FUN__text__00422360(0);
  } while ((local_10 & 0xff) != 0);
  FUN__text__004d0750();
  local_14 = DAT_007e0f04;
  if (DAT_007e0f04 != -1) {
    FUN__text__00439e30(DAT_007e0f04);
  }
  (**(code **)(*local_8 + 4))();
  FUN__text__0056ce80();
  local_8 = (int *)0x4d1b31;
  FUN__text__0056ce80();
  return;
}

