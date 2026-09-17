
void FUN__text__00442a50(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 8);
  iVar2 = FUN__text__00419450();
  if (iVar2 != 0) {
    iVar2 = FUN__text__00424f80("SysDx->IsServer() == 0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                DAT_005ffc94 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*(char *)(local_c + 0xd) != '\a') {
    iVar2 = FUN__text__00424f80("set->Head.DataKind == DxPlayDataKindAllied",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                DAT_005ffc94 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    *(undefined1 *)(local_8 + local_10 + 0x1a8c) = *(undefined1 *)(local_c + local_10 + 0x12);
  }
  local_8 = 0x442b1c;
  FUN__text__0056ce80();
  return;
}

