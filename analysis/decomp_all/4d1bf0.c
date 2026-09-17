
void FUN__text__004d1bf0(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_GDI32_DLL_DeleteObject)(*param_1);
  iVar2 = FUN__text__0056ce80();
  if (iVar2 == 0) {
    iVar2 = FUN__text__00424f80("DeleteObject( *adr ) != 0",
                                "e:\\crosshermit\\game\\src\\yoshimaru\\ysub.cpp",DAT_00624ad8 + 7,0
                               );
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_c = 0x4d1c57;
  FUN__text__0056ce80();
  return;
}

