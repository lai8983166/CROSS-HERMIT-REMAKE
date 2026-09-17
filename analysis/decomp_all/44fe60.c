
void __fastcall FUN__text__0044fe60(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  undefined4 *local_28;
  undefined4 *local_24;
  undefined4 *local_20;
  undefined4 *local_1c;
  undefined4 *local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__0058f6b2;
  local_10 = ExceptionList;
  puVar2 = local_68;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_005986a0;
  local_8 = 6;
  local_14 = param_1;
  FUN__text__0044ffa0();
  local_8._0_1_ = 5;
  FUN__text__00428bc0();
  local_8._0_1_ = 4;
  if (local_14 == (undefined4 *)0x0) {
    local_18 = (undefined4 *)0x0;
  }
  else {
    local_18 = local_14 + 0x60;
  }
  FUN__text__004257c0();
  local_8._0_1_ = 3;
  if (local_14 == (undefined4 *)0x0) {
    local_1c = (undefined4 *)0x0;
  }
  else {
    local_1c = local_14 + 0x19;
  }
  FUN__text__004215f0();
  local_8._0_1_ = 2;
  if (local_14 == (undefined4 *)0x0) {
    local_20 = (undefined4 *)0x0;
  }
  else {
    local_20 = local_14 + 0xd;
  }
  FUN__text__004234d0();
  local_8._0_1_ = 1;
  if (local_14 == (undefined4 *)0x0) {
    local_24 = (undefined4 *)0x0;
  }
  else {
    local_24 = local_14 + 0xd;
  }
  FUN__text__00429340();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__004246c0();
  local_8 = 0xffffffff;
  if (local_14 == (undefined4 *)0x0) {
    local_28 = (undefined4 *)0x0;
  }
  else {
    local_28 = local_14 + 4;
  }
  FUN__text__00439d90();
  ExceptionList = local_10;
  local_8 = 0x44ff99;
  FUN__text__0056ce80();
  return;
}

