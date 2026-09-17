
void FUN__text__00497210(int param_1,undefined1 param_2)

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
  if (DAT_007a49f8 == 0) {
    iVar2 = FUN__text__00424f80("ScriptWork!=0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fa0 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_1 < 0) || (99 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=cellno)&&(cellno<=99)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fa0 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined1 *)(DAT_007a49f8 + 0x19 + param_1 * 4) = param_2;
  uStack_8 = 0x4972a1;
  FUN__text__0056ce80();
  return;
}

