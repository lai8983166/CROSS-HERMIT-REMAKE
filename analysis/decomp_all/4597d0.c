
void __fastcall FUN__text__004597d0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  uint local_8;
  
  puStack_c = &LAB__text__0058f855;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_0059a838;
  local_8 = 1;
  local_14 = param_1;
  FUN__text__0041d280();
  FUN__text__0040d610();
  FUN__text__0041f4e0(0x5a);
  local_8 = local_8 & 0xffffff00;
  FUN__text__00407710();
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  local_8 = 0x45987c;
  FUN__text__0056ce80();
  return;
}

