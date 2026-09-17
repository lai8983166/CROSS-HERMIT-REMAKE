
void __fastcall FUN__text__004ab650(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__005902a0;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_005a0a40;
  local_8 = 6;
  local_14 = param_1;
  FUN__text__0041f4e0(0xc);
  FUN__text__004d1bf0(local_14 + 0x1e53);
  FUN__text__004d0750();
  local_8._0_1_ = 5;
  FUN__text__004d6010();
  local_8._0_1_ = 4;
  FUN__text__004d6010();
  local_8._0_1_ = 3;
  FUN__text__004d6010();
  local_8._0_1_ = 2;
  FUN__text__004d66e0();
  local_8._0_1_ = 1;
  FUN__text__00407710();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__00464cc0();
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  local_8 = 0x4ab752;
  FUN__text__0056ce80();
  return;
}

