
void FUN__text__004ab570(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__00590231;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  FUN__text__00464c60();
  local_8._0_1_ = 1;
  FUN__text__004075e0();
  local_8._0_1_ = 2;
  FUN__text__004d66a0();
  local_8._0_1_ = 3;
  FUN__text__004d5fb0();
  local_8._0_1_ = 4;
  FUN__text__004d5fb0();
  local_8 = CONCAT31(local_8._1_3_,5);
  FUN__text__004d5fb0();
  *local_14 = &PTR_DAT_005a0a40;
  ExceptionList = local_10;
  local_8 = 0x4ab640;
  FUN__text__0056ce80();
  return;
}

