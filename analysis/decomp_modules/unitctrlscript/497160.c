
void FUN__text__00497160(int param_1,undefined2 param_2,undefined2 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_1 == 0) {
    *(undefined2 *)(DAT_007a49f8 + 0x10) = param_2;
    *(undefined2 *)(DAT_007a49f8 + 0x12) = param_3;
  }
  else if (param_1 == 1) {
    *(undefined2 *)(DAT_007a49f8 + 0x14) = param_2;
    *(undefined2 *)(DAT_007a49f8 + 0x16) = param_3;
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619f9c + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x497201;
  FUN__text__0056ce80();
  return;
}

