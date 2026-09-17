
void FUN__text__0042be70(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  uint local_8;
  
  puStack_c = &LAB__text__0058f001;
  local_10 = ExceptionList;
  puVar2 = local_58;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 1;
  ExceptionList = &local_10;
  FUN__text__0042bf00();
  local_8 = local_8 & 0xffffff00;
  if (local_14 == 0) {
    local_18 = 0;
  }
  else {
    local_18 = local_14 + 0x28;
  }
  FUN__text__00422640();
  local_8 = 0xffffffff;
  FUN__text__0041f9e0();
  ExceptionList = local_10;
  local_8 = 0x42befb;
  FUN__text__0056ce80();
  return;
}

