
void FUN__text__00443c10(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f370;
  local_10 = ExceptionList;
  puVar4 = local_58;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  FUN__text__004075e0();
  local_8._0_1_ = 1;
  FUN__text__004075e0();
  local_8._0_1_ = 2;
  FUN__text__004075e0();
  local_8._0_1_ = 3;
  _eh_vector_constructor_iterator_
            (local_14 + 0x6e,0x80,0x14,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 4;
  _eh_vector_constructor_iterator_(local_14 + 0x2ee,0x80,4,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 5;
  _eh_vector_constructor_iterator_(local_14 + 0x36e,0x8c,2,FUN__text__00409300,FUN__text__00409360);
  local_8._0_1_ = 6;
  FUN__text__00425090();
  local_8._0_1_ = 7;
  FUN__text__00441270();
  local_8._0_1_ = 8;
  FUN__text__00428120();
  local_8._0_1_ = 9;
  _eh_vector_constructor_iterator_(local_14 + 0x2298,8,2,FUN__text__00428120,FUN__text__00428160);
  local_8._0_1_ = 10;
  _eh_vector_constructor_iterator_(local_14 + 0x22a0,8,4,FUN__text__00428120,FUN__text__00428160);
  local_8._0_1_ = 0xb;
  FUN__text__00428120();
  local_8 = CONCAT31(local_8._1_3_,0xc);
  *local_14 = &PTR_DAT_00598318;
  uVar2 = FUN__text__004e2c30();
  local_14[0xd] = uVar2;
  _memset(local_14 + 0x695,0,0x5c);
  _memset(local_14 + 0x6ec,0,0x10);
  _memset(local_14 + 0x2296,0,8);
  _memset(local_14 + 0x229c,0,0x10);
  FUN__text__00444780();
  FUN__text__004077c0(DAT_007a49fc);
  local_14[0x694] = 0;
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  local_14[0x6e8] = uVar2;
  if (local_14[0x6e8] == 0) {
    iVar3 = FUN__text__00424f80("tFont0!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060670c + 0x11,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  local_14[0x6e9] = uVar2;
  if (local_14[0x6e9] == 0) {
    iVar3 = FUN__text__00424f80("tFont1!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060670c + 0x17,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_GDI32_DLL_CreateFontA)(0x12,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  local_14[0x6ea] = uVar2;
  if (local_14[0x6ea] == 0) {
    iVar3 = FUN__text__00424f80("tFont2!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060670c + 0x1b,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_GDI32_DLL_CreateFontA)(0x10,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  local_14[0x6eb] = uVar2;
  if (local_14[0x6eb] == 0) {
    iVar3 = FUN__text__00424f80("tFont3!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060670c + 0x1f,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_18 = 0; local_18 != 2; local_18 = local_18 + 1) {
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00409480(local_14[0x6ea]);
  }
  FUN__text__004251e0(DAT_007a49fc,10,local_14[0x6eb]);
  FUN__text__00443bb0(0);
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  FUN__text__0056ce80();
  return;
}

