
void __fastcall FUN__text__0045a4b0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [7];
  undefined4 uStack_38;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__0058f94b;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_0059aa40;
  local_8 = 4;
  local_14 = param_1;
  FUN__text__0056de40(param_1 + 0x8a0,0x80,10,FUN__text__00407710);
  local_8._0_1_ = 3;
  FUN__text__00464cc0();
  local_8._0_1_ = 2;
  FUN__text__0041eb30();
  local_8._0_1_ = 1;
  FUN__text__0056de40(local_14 + 0x64c,0x8c,10,FUN__text__00409360);
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__0056de40(local_14 + 0xc,0x80,0x32,FUN__text__00407710);
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  uStack_38 = 0x45a592;
  FUN__text__0056ce80();
  return;
}

