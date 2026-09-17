
void FUN__text__00474fb0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  void *local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (void *)(param_1 + 0x290);
  _memset(local_c,0,0x5c);
  if (*(byte *)(*(int *)(param_1 + 600) + 0xa4) < 4) {
    *(undefined1 *)((int)local_c + 0x17) = 0;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x9f) = 2;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xa0) = 0;
    if ((*(char *)((int)local_c + 0x18) != '\0') &&
       (iVar2 = FUN__text__00424f80("ai->ai_tblno==0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618de8 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    puVar3 = (undefined4 *)(&DAT_00618c48 + *(char *)((int)local_c + 0x18) * 0x40);
    puVar4 = (undefined4 *)((int)local_c + 0x1c);
    for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
  }
  else {
    *(undefined1 *)((int)local_c + 0x17) = 1;
    puVar3 = (undefined4 *)(&DAT_00618c88 + *(char *)((int)local_c + 0x18) * 0x40);
    puVar4 = (undefined4 *)((int)local_c + 0x1c);
    for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
  }
  local_8 = 0x4750a4;
  FUN__text__0056ce80();
  return;
}

