
void FUN__text__00422c60(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [15];
  undefined4 uStack_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_GetClientRect)(param_1,&local_1c);
  FUN__text__0056ce80();
  (*API_GDI32_DLL_CreateRectRgn)(local_1c,local_18,local_14,local_10);
  local_c = FUN__text__0056ce80();
  uStack_20 = 0x422cc6;
  FUN__text__0056ce80();
  return;
}

