
void FUN__text__00431cc0(int param_1)

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
  if ((param_1 + -1 < 0) || (0xf9 < param_1 + -1)) {
    iVar2 = FUN__text__00424f80("(0<=enemy_no) && (enemy_no<(250))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                DAT_005ff744 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x431d2e;
  FUN__text__0056ce80();
  return;
}

