
void FUN__text__004da7f0(int param_1)

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
  if ((param_1 < 0) || (399 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=scenario_no&&(scenario_no<=399))",
                                "E:\\CrossHermit\\GAME\\SRC\\COMMON\\ComRound.cpp",DAT_006ad1c8 + 1,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_8 = 0x4da852;
  FUN__text__0056ce80();
  return;
}

