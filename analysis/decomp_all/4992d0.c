
void FUN__text__004992d0(int param_1)

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
    FUN__text__00467850(1,0);
  }
  else if (param_1 == 1) {
    FUN__text__00467850(2,1);
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_0059ea68,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_0061a010 + 0xc,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x499364;
  FUN__text__0056ce80();
  return;
}

