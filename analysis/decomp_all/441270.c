
void FUN__text__00441270(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [5];
  undefined4 uStack_40;
  int *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f1e7;
  local_10 = ExceptionList;
  puVar3 = local_54;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  _eh_vector_constructor_iterator_
            (local_14 + 0x21,0x8c,0x14,FUN__text__00409300,FUN__text__00409360);
  local_8 = CONCAT31(local_8._1_3_,1);
  (*API_GDI32_DLL_CreateFontA)(0x10,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  iVar2 = FUN__text__0056ce80();
  *local_14 = iVar2;
  if (*local_14 == 0) {
    iVar2 = FUN__text__00424f80("tFont!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\MesBox.cpp",
                                DAT_005ffc68 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  uStack_40 = 0x44135a;
  FUN__text__0056ce80();
  return;
}

