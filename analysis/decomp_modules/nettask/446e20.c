
void __fastcall FUN__text__00446e20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x1bde) = 0x118;
  *(undefined1 *)(param_1 + 0x1bdc) = 0xff;
  *(undefined4 *)(param_1 + 0x1bcc) = 0;
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1bd0),0,0xc);
  local_8 = 0x446e82;
  FUN__text__0056ce80();
  return;
}

