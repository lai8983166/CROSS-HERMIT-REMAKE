
void __fastcall FUN__text__00454c80(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  char *local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x44);
  if (*local_c != '\x03') {
    local_8 = param_1;
    iVar2 = FUN__text__00424f80("wk->prog_no==3",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd90 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c[0x14] = '\x01';
  local_8 = 0x454ce9;
  FUN__text__0056ce80();
  return;
}

