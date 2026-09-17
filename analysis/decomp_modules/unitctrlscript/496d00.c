
void FUN__text__00496d00(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (DAT_007a49f8 == 0) {
    iVar2 = FUN__text__00424f80("ScriptWork!=0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619f88 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (DAT_007a49f8 != 0) {
    local_8 = DAT_007a49f8;
    FUN__text__00428ad0(DAT_007a49f8);
    DAT_007a49f8 = 0;
  }
  local_8 = 0x496d7a;
  FUN__text__0056ce80();
  return;
}

