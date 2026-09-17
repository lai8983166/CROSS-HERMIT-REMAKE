
void __fastcall FUN__text__00444060(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__0058f470;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_00598318;
  local_8 = 0xc;
  local_14 = param_1;
  FUN__text__0040d120(0x13);
  FUN__text__00446290(local_14 + 0x2296);
  FUN__text__00446290(local_14 + 0x229c);
  FUN__text__00446290(local_14 + 0x229e);
  if (local_14[0x6e8] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_14[0x6e8]);
    FUN__text__0056ce80();
    local_14[0x6e8] = 0;
  }
  if (local_14[0x6e9] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_14[0x6e9]);
    FUN__text__0056ce80();
    local_14[0x6e9] = 0;
  }
  if (local_14[0x6ea] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_14[0x6ea]);
    FUN__text__0056ce80();
    local_14[0x6ea] = 0;
  }
  if (local_14[0x6eb] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_14[0x6eb]);
    FUN__text__0056ce80();
    local_14[0x6eb] = 0;
  }
  local_8._0_1_ = 0xb;
  FUN__text__00428160();
  local_8._0_1_ = 10;
  FUN__text__0056de40(local_14 + 0x22a0,8,4,FUN__text__00428160);
  local_8._0_1_ = 9;
  FUN__text__0056de40(local_14 + 0x2298,8,2,FUN__text__00428160);
  local_8._0_1_ = 8;
  FUN__text__00428160();
  local_8._0_1_ = 7;
  FUN__text__00441360();
  local_8._0_1_ = 6;
  FUN__text__004250d0();
  local_8._0_1_ = 5;
  FUN__text__0056de40(local_14 + 0x36e,0x8c,2,FUN__text__00409360);
  local_8._0_1_ = 4;
  FUN__text__0056de40(local_14 + 0x2ee,0x80,4,FUN__text__00407710);
  local_8._0_1_ = 3;
  FUN__text__0056de40(local_14 + 0x6e,0x80,0x14,FUN__text__00407710);
  local_8._0_1_ = 2;
  FUN__text__00407710();
  local_8._0_1_ = 1;
  FUN__text__00407710();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__00407710();
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  FUN__text__0056ce80();
  return;
}

