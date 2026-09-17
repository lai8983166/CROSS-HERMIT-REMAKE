
void FUN__text__0044c390(uint param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined **local_14;
  undefined **local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (0x7f < param_1) {
    iVar2 = FUN__text__00424f80("sno < (sizeof(NetworkScenarioData) / sizeof(SysNetScenarioData))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_0060678c + 5,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (3 < param_2) {
    iVar2 = FUN__text__00424f80("no < 4","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060678c + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__0044c200(param_1);
  if ((*(short *)(local_c + 4) < 0) || (0x45 < *(ushort *)(local_c + 4))) {
    iVar2 = FUN__text__00424f80("(0<=sce->NameNo) && (sce->NameNo<(sizeof(NetworkScenarioExp) / sizeof(SysNetScenarioExplain)))"
                                ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_0060678c + 10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = &PTR_DAT_006001b0 + *(short *)(local_c + 4) * 0x51;
  local_14 = &PTR_DAT_006001b4 + *(short *)(local_c + 4) * 0x51 + param_2 * 0x14;
  local_8 = 0x44c483;
  FUN__text__0056ce80();
  return;
}

