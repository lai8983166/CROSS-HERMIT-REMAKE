
void FUN__text__004d1730(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0059077b;
  local_10 = ExceptionList;
  puVar3 = local_5c;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  local_18 = FUN__text__00428a40(0x30);
  local_8 = 0;
  if (local_18 == 0) {
    local_1c = 0;
  }
  else {
    local_1c = FUN__text__004d1910();
  }
  local_14 = local_1c;
  local_8 = 0xffffffff;
  DAT_007a4e40 = local_1c;
  *(undefined1 *)(local_1c + 0x28) = 1;
  if (DAT_007a4e40 == 0) {
    iVar2 = FUN__text__00424f80("tTask!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIMARU\\YBC\\YbcTask.cpp"
                                ,DAT_00624ad0 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (DAT_007a4e40 != 0) {
    FUN__text__004216c0(DAT_007a4e40,0,1);
  }
  ExceptionList = local_10;
  local_8 = 0x4d1813;
  FUN__text__0056ce80();
  return;
}

