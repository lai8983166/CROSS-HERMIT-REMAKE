
void __fastcall FUN__text__004d1960(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB__text__005907b9;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_005c306c;
  local_8 = 0;
  local_14 = param_1;
  FUN__text__004d19e0(0);
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  local_8 = 0x4d19d4;
  FUN__text__0056ce80();
  return;
}

