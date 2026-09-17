
void FUN__text__0044d370(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f4f5;
  local_10 = ExceptionList;
  puVar2 = local_58;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439ef0();
  local_8 = 0;
  FUN__text__004075e0();
  local_8 = CONCAT31(local_8._1_3_,1);
  *local_14 = &PTR_DAT_005985f4;
  _memset(local_14 + 0xc,0,8);
  for (local_18 = 0; local_18 != 4; local_18 = local_18 + 1) {
    local_14[local_18 + 0xe] = 0xffffffff;
  }
  FUN__text__0044d610();
  ExceptionList = local_10;
  local_8 = 0x44d42d;
  FUN__text__0056ce80();
  return;
}

