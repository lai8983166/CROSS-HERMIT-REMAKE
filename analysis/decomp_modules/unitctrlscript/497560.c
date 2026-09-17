
void FUN__text__00497560(void)

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
                                DAT_00619fac + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = DAT_007a49f4 + 0x80c7c + local_8 * 0x520;
  iVar2 = FUN__text__00468d10(local_c);
  if (iVar2 != 1) {
    iVar2 = FUN__text__00424f80("tTask->UnitCt.IsUwUsed(wk)==1",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fac + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x497628;
  FUN__text__0056ce80();
  return;
}

