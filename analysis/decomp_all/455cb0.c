
void FUN__text__00455cb0(undefined1 *param_1)

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
  _memset(param_1,0,0x10);
  *param_1 = 0xff;
  local_8 = 0x455cf0;
  FUN__text__0056ce80();
  return;
}

