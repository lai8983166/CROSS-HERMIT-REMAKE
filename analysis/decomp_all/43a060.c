
void FUN__text__0043a060(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f176;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00420990();
  local_8 = 0;
  FUN__text__004075e0();
  local_8._0_1_ = 1;
  FUN__text__004075e0();
  local_8._0_1_ = 2;
  FUN__text__004075e0();
  local_8 = CONCAT31(local_8._1_3_,3);
  *local_14 = 0;
  local_14[1] = 0;
  local_14[0x23] = 0;
  local_14[0x24] = 0;
  local_14[0x25] = 0;
  local_14[0x9967] = 0;
  local_14[0x9968] = 0;
  local_14[0x98ec] = 0;
  local_14[0x98ed] = 0xffffffff;
  local_14[0x9963] = 0;
  *(undefined2 *)((int)local_14 + 0x265b2) = 1;
  *(undefined2 *)(local_14 + 0x996d) = 1;
  *(undefined2 *)(local_14 + 0x9979) = 0xffff;
  *(undefined2 *)((int)local_14 + 0x265e6) = 0xffff;
  local_14[0x9976] = 0;
  local_14[0x9977] = 1;
  *(undefined1 *)((int)local_14 + 0x26595) = 0;
  *(undefined1 *)((int)local_14 + 0x26596) = 0;
  *(undefined1 *)((int)local_14 + 0x26597) = 0;
  *(undefined1 *)(local_14 + 0x9966) = 0;
  local_14[0x26] = 0;
  local_14[0x27] = 0;
  local_14[0x28] = 0;
  local_14[0x29] = 0;
  local_14[0x2a] = 0;
  *(undefined1 *)(local_14 + 0x997c) = 0;
  local_14[0x98ee] = 0;
  local_14[0x98ef] = 0;
  *(undefined2 *)(local_14 + 0x98f1) = 0;
  FUN__text__0043ab10();
  ExceptionList = local_10;
  local_8 = 0x43a25e;
  FUN__text__0056ce80();
  return;
}

