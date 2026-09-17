
void FUN__text__004b8a90(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [5];
  undefined4 uStack_40;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005903ae;
  local_10 = ExceptionList;
  puVar3 = local_54;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  FUN__text__004d5fb0();
  local_8._0_1_ = 1;
  FUN__text__004d5fb0();
  local_8._0_1_ = 2;
  FUN__text__004d5fb0();
  local_8._0_1_ = 3;
  FUN__text__004d5fb0();
  local_8._0_1_ = 4;
  _eh_vector_constructor_iterator_
            (local_14 + 0x6748,0x6424,5,FUN__text__004d5fb0,FUN__text__004d6010);
  local_8._0_1_ = 5;
  FUN__text__004d66a0();
  local_8._0_1_ = 6;
  FUN__text__00464c60();
  local_8 = CONCAT31(local_8._1_3_,7);
  FUN__text__004075e0();
  *local_14 = &PTR_DAT_005a0c18;
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar1 = FUN__text__0056ce80();
  local_14[0x323] = uVar1;
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  uStack_40 = 0x4b8bd2;
  FUN__text__0056ce80();
  return;
}

