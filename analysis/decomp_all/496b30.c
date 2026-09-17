
void FUN__text__00496b30(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  void *local_c;
  void *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (void *)FUN__text__00428a40(0x24c4);
  local_8 = local_c;
  if (local_c == (void *)0x0) {
    iVar2 = FUN__text__00424f80("pt!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619f7c + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  DAT_007a49f8 = local_8;
  _memset(local_8,0,0x24c4);
  local_8 = (void *)0x496bb4;
  FUN__text__0056ce80();
  return;
}

