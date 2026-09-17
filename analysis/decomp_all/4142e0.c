
void FUN__text__004142e0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                              DAT_005ff534 + 2,0);
  if (iVar2 == 0) {
    local_8 = 0x414339;
    FUN__text__0056ce80();
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

