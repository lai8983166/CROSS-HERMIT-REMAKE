
void FUN__text__0044c200(uint param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined **local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (0x7f < param_1) {
    iVar2 = FUN__text__00424f80("sno < (sizeof(NetworkScenarioData) / sizeof(SysNetScenarioData))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606784 + 3,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = &PTR_DAT_005ffcb0 + param_1 * 2;
  local_8 = 0x44c267;
  FUN__text__0056ce80();
  return;
}

