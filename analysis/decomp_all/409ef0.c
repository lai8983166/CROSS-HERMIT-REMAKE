
void FUN__text__00409ef0(undefined1 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_1,0,0x58);
  *param_1 = 1;
  *(undefined2 *)(param_1 + 0xc) = 0xffff;
  *(undefined4 *)(param_1 + 0x1c) = local_8;
  *(undefined1 **)(param_1 + 0x24) = param_1;
  *(undefined2 *)(param_1 + 0x10) = 0;
  param_1[0x56] = 0x80;
  param_1[0x55] = 0x80;
  param_1[0x54] = 0x80;
  local_8 = 0x409f69;
  FUN__text__0056ce80();
  return;
}

