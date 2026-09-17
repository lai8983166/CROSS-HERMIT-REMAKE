
void FUN__text__00496c60(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
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
                                DAT_00619f84 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_8 = 0; local_8 != param_2; local_8 = local_8 + 1) {
    puVar3 = (undefined4 *)(param_1 + local_8 * 0x20);
    puVar4 = (undefined4 *)(DAT_007a49f8 + 0x1a8 + local_8 * 0x20);
    for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
  }
  local_8 = 0x496cf3;
  FUN__text__0056ce80();
  return;
}

