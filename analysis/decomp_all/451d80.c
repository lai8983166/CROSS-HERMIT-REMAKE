
void __fastcall FUN__text__00451d80(int param_1)

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
  *(char *)(param_1 + 0x40) = *(char *)(param_1 + 0x40) + -1;
  if (*(byte *)(param_1 + 0x40) < 0x81) {
    *(undefined1 *)(param_1 + 0x40) = 0x80;
    *(char *)(param_1 + 0x41) = *(char *)(param_1 + 0x41) + -1;
    if (*(byte *)(param_1 + 0x40) < 0x81) {
      *(undefined1 *)(param_1 + 0x41) = 0x80;
    }
  }
  local_8 = param_1;
  FUN__text__00451e20();
  FUN__text__00415420();
  FUN__text__00422360(0);
  local_8 = 0x451e15;
  FUN__text__0056ce80();
  return;
}

