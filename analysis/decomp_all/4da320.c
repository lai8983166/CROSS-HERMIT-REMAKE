
void __fastcall FUN__text__004da320(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [11];
  undefined4 uStack_28;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB__text__005909c9;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 0;
  ExceptionList = &local_10;
  local_14 = param_1;
  FUN__text__0056de40(param_1 + 0xce4,0x80,10,FUN__text__00407710);
  local_8 = 0xffffffff;
  FUN__text__0056de40(local_14 + 0x34,0x80,10,FUN__text__00407710);
  ExceptionList = local_10;
  uStack_28 = 0x4da3a9;
  FUN__text__0056ce80();
  return;
}

