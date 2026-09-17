
void FUN__text__00504d70(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__00590aa8;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  FUN__text__004075e0();
  local_8 = CONCAT31(local_8._1_3_,1);
  _eh_vector_constructor_iterator_(local_14 + 0x98,0x54,10,FUN__text__00464c60,FUN__text__00464cc0);
  *local_14 = &PTR_DAT_005ca9d0;
  ExceptionList = local_10;
  local_8 = 0x504e09;
  FUN__text__0056ce80();
  return;
}

