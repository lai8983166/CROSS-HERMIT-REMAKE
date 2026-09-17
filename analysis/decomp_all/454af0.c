
void FUN__text__00454af0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 2) || (0x10 < param_1)) {
    iVar2 = FUN__text__00424f80("(UnitEventScriptPerfect<=code) && (code<=UnitEventScriptBadLuck2)",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd8c + 0x14,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_2 < 2) || (0x10 < param_2)) {
    iVar2 = FUN__text__00424f80("(UnitEventScriptPerfect<=same) && (same<=UnitEventScriptBadLuck2)",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd8c + 0x15,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__00454bb0(1,0,param_2);
  *(undefined4 *)(local_8 + 0x174) = *(undefined4 *)(&DAT_0060ca7c + param_1 * 4);
  local_8 = 0x454ba3;
  FUN__text__0056ce80();
  return;
}

