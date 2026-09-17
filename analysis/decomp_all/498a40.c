
void FUN__text__00498a40(void)

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
  local_8 = FUN__text__00497500();
  if ((local_8 < 0) || (0xf9 < local_8)) {
    iVar2 = FUN__text__00424f80("(0<=unitno) && (unitno<(250))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619ff0 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__004801e0(local_8);
  local_8 = 0x498ab5;
  FUN__text__0056ce80();
  return;
}

