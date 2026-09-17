
void FUN__text__00497630(void)

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
  local_8 = FUN__text__00497500();
  if ((local_8 < 0) || (0xfa < local_8)) {
    iVar2 = FUN__text__00424f80("(0<=no) && (no<=(250))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fb0 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = 0xfa - local_8;
  if ((local_c < 1) || (0xfa < local_c)) {
    iVar2 = FUN__text__00424f80("(1<=eno) && (eno<((250)+1))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fb0 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4976d1;
  FUN__text__0056ce80();
  return;
}

