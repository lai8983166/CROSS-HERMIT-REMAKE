
void __fastcall FUN__text__004d9c00(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [15];
  undefined4 uStack_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__0059097e;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_005c8388;
  local_8 = 5;
  local_14 = param_1;
  FUN__text__0041f4e0(0x12);
  FUN__text__004d1bf0(local_14 + 0x66ac);
  FUN__text__004d1bf0(local_14 + 0x66ad);
  local_8._0_1_ = 4;
  FUN__text__004d66e0();
  local_8._0_1_ = 3;
  FUN__text__004d6010();
  local_8._0_1_ = 2;
  FUN__text__004d6010();
  local_8._0_1_ = 1;
  FUN__text__004d6010();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__0056de40(local_14 + 0xc,0x8c,2,FUN__text__00409360);
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  uStack_18 = 0x4d9d07;
  FUN__text__0056ce80();
  return;
}

