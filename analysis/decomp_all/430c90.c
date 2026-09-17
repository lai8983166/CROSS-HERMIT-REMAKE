
void __thiscall FUN__text__00430c90(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < 0) || (0x1f < param_2)) {
    iVar2 = FUN__text__00424f80("(0<=eno) && (eno<32)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                DAT_005ff738 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_3 < 0) || (0xf < param_3)) {
    iVar2 = FUN__text__00424f80("(_UnitDataPlayer1P<=player) && (player<=_UnitDataPlayerCpu12)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                DAT_005ff738 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = local_8 + 0x2e714 + param_2 * 0x40 + param_3 * 4;
  local_8 = 0x430d39;
  FUN__text__0056ce80();
  return;
}

