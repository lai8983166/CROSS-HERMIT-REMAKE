
void FUN__text__0045a3b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f8db;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  _eh_vector_constructor_iterator_(local_14 + 0xc,0x80,0x32,FUN__text__004075e0,FUN__text__00407710)
  ;
  local_8._0_1_ = 1;
  _eh_vector_constructor_iterator_(local_14 + 0x64c,0x8c,10,FUN__text__00409300,FUN__text__00409360)
  ;
  local_8._0_1_ = 2;
  FUN__text__0041ead0();
  local_8._0_1_ = 3;
  FUN__text__00464c60();
  local_8 = CONCAT31(local_8._1_3_,4);
  _eh_vector_constructor_iterator_(local_14 + 0x8a0,0x80,10,FUN__text__004075e0,FUN__text__00407710)
  ;
  *local_14 = &PTR_DAT_0059aa40;
  ExceptionList = local_10;
  local_8 = 0x45a4a4;
  FUN__text__0056ce80();
  return;
}

