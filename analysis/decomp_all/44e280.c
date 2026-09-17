
void FUN__text__0044e280(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f529;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00420990();
  local_8 = 0;
  FUN__text__00439380();
  *local_14 = 0;
  local_14[1] = 0;
  local_14[2] = 0;
  _memset(local_14 + 0x2b,0,0x28);
  ExceptionList = local_10;
  local_8 = 0x44e31f;
  FUN__text__0056ce80();
  return;
}

