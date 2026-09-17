
void FUN__text__00498e00(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                              DAT_0061a000 + 1,0);
  if (iVar2 == 0) {
    uStack_8 = 0x498e52;
    FUN__text__0056ce80();
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

