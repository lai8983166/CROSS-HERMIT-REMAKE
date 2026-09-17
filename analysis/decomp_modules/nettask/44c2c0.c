
void FUN__text__0044c2c0(uint param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined **local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (0x7f < param_1) {
    iVar2 = FUN__text__00424f80("sno < (sizeof(NetworkScenarioData) / sizeof(SysNetScenarioData))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606788 + 4,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__0044c200(param_1);
  if ((*(short *)(local_c + 4) < 0) || (0x45 < *(ushort *)(local_c + 4))) {
    iVar2 = FUN__text__00424f80("(0<=sce->NameNo) && (sce->NameNo<(sizeof(NetworkScenarioExp) / sizeof(SysNetScenarioExplain)))"
                                ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606788 + 8
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = &PTR_DAT_006001b0 + *(short *)(local_c + 4) * 0x51;
  local_8 = 0x44c37c;
  FUN__text__0056ce80();
  return;
}

