
void FUN__text__00409900(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058eba9;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00420990();
  local_8 = 0;
  FUN__text__0041ead0();
  *local_14 = 0;
  local_14[1] = 0;
  local_14[2] = 0;
  local_14[3] = 0;
  local_14[4] = 0;
  local_14[5] = 0;
  local_14[0xb] = 0;
  local_14[0xc] = 0;
  local_14[0xd] = 0;
  local_14[0xe] = 0;
  local_14[0xf] = 0;
  local_14[0x10] = 0xffffffff;
  ExceptionList = local_10;
  local_8 = 0x4099e4;
  FUN__text__0056ce80();
  return;
}

