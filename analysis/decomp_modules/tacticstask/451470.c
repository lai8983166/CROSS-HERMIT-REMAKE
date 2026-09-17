
void __fastcall FUN__text__00451470(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__0058f7cd;
  local_10 = ExceptionList;
  puVar2 = local_5c;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_0059a430;
  local_8 = 5;
  local_14 = param_1;
  FUN__text__0041d280();
  FUN__text__0040d610();
  FUN__text__004ce060();
  FUN__text__004d0790(0);
  FUN__text__00496d00();
  if (local_14[0x19] != 0) {
    local_1c = local_14[0x19];
    FUN__text__00428ad0(local_1c);
    local_14[0x19] = 0;
  }
  FUN__text__0040d120(1);
  for (local_18 = 0; local_18 != 0xd; local_18 = local_18 + 1) {
    FUN__text__0040d120(local_18 + 7);
  }
  if (local_14[0x45fc9] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_14[0x45fc9]);
    FUN__text__0056ce80();
    local_14[0x45fc9] = 0;
  }
  FUN__text__00465e60();
  local_8._0_1_ = 4;
  FUN__text__004250d0();
  local_8._0_1_ = 3;
  FUN__text__0056de40(local_14 + 0x45fca,0x8c,2,FUN__text__00409360);
  local_8._0_1_ = 2;
  FUN__text__00465bc0();
  local_8._0_1_ = 1;
  FUN__text__00407710();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__00407710();
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  local_18 = 0x451625;
  FUN__text__0056ce80();
  return;
}

