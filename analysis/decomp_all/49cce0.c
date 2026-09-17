
void __fastcall FUN__text__0049cce0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (int)*(char *)(param_1 + 0x115cb8);
  local_8 = param_1;
  switch(local_c) {
  case 0:
    FUN__text__0049cdc0(0);
    break;
  case 1:
  case 2:
    if (*(short *)(param_1 + 0x109d4e) == -1) {
      FUN__text__0049cdc0(0);
    }
    else {
      FUN__text__0049cdc0(1);
    }
    FUN__text__0049d160(0x24,0x2e0,0xc3);
    break;
  case 3:
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                DAT_0061b000 + 0x11,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x49cd9d;
  FUN__text__0056ce80();
  return;
}

