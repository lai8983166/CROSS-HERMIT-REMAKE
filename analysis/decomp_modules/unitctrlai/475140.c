
void FUN__text__00475140(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  *(undefined1 *)(param_1 + 0x2a7) = 0;
  *(undefined1 *)(*(int *)(param_1 + 600) + 0x9f) = 2;
  *(undefined1 *)(*(int *)(param_1 + 600) + 0xa0) = 0;
  if (*(char *)(param_1 + 0x2a8) != '\0') {
    iVar2 = FUN__text__00424f80("ai->ai_tblno==0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618dec + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  puVar3 = (undefined4 *)(&DAT_00618c48 + *(char *)(local_c + 0x18) * 0x40);
  puVar4 = (undefined4 *)(local_c + 0x1c);
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  local_8 = 0x4751e8;
  FUN__text__0056ce80();
  return;
}

