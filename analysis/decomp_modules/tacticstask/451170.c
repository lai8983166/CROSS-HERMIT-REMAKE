
void FUN__text__00451170(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [6];
  undefined4 uStack_40;
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f75d;
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
  FUN__text__004653d0();
  local_8._0_1_ = 3;
  _eh_vector_constructor_iterator_
            (local_14 + 0x45fca,0x8c,2,FUN__text__00409300,FUN__text__00409360);
  local_8._0_1_ = 4;
  FUN__text__00425090();
  local_8 = CONCAT31(local_8._1_3_,5);
  *local_14 = &PTR_DAT_0059a430;
  local_14[0xd] = 0;
  local_14[0x5e] = 0;
  local_14[0x5f] = 0;
  local_14[0x60] = 4;
  local_14[0x62] = 0;
  local_14[0x61] = 0;
  (*API_GDI32_DLL_CreateFontA)(10,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  local_14[0x45fc9] = uVar2;
  if (local_14[0x45fc9] == 0) {
    iVar3 = FUN__text__00424f80("hFontChat!=0",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd68 + 0x10,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_18 = 0; local_18 != 2; local_18 = local_18 + 1) {
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00409480(local_14[0x45fc9]);
  }
  FUN__text__004251e0(DAT_007a49fc,4,local_14[0x45fc9]);
  FUN__text__00425420(1);
  *(undefined1 *)(local_14 + 0x45fc8) = 0;
  *(undefined1 *)(local_14 + 99) = 0;
  *(undefined1 *)((int)local_14 + 0x18d) = 0;
  *(undefined1 *)(local_14 + 0x5c) = 0;
  *(undefined1 *)((int)local_14 + 0x171) = 0;
  *(undefined1 *)((int)local_14 + 0x172) = 0;
  _memset(local_14 + 0x45f76,0,0x140);
  *(undefined1 *)((int)local_14 + 0x43) = 0;
  _memset(local_14 + 0x11,0,0x1c);
  FUN__text__00496af0(local_14);
  uVar2 = FUN__text__00496b30();
  local_14[0x18] = uVar2;
  FUN__text__00496bc0();
  FUN__text__00455310();
  FUN__text__00455c20();
  FUN__text__00455810();
  FUN__text__004562f0();
  local_14[0x19] = 0;
  FUN__text__00465f90(local_14);
  *(undefined1 *)(local_14 + 0xc) = 0;
  *(undefined1 *)((int)local_14 + 0x31) = 0;
  FUN__text__004e26e0();
  DAT_005ff720 = 0xffffffff;
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  uStack_40 = 0x451466;
  FUN__text__0056ce80();
  return;
}

