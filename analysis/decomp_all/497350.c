
void FUN__text__00497350(uint param_1,uint param_2)

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
  if (DAT_007a49f8 == 0) {
    iVar2 = FUN__text__00424f80("ScriptWork!=0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fa8 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (((int)param_1 < 0) || (99 < (int)param_1)) {
    iVar2 = FUN__text__00424f80("(0<=src_no)&&(src_no<100)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fa8 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (((int)param_2 < 0) || (99 < (int)param_2)) {
    iVar2 = FUN__text__00424f80("(0<=dst_no)&&(dst_no<100)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fa8 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (param_1 != param_2) {
    for (local_8 = 0; local_8 != 100; local_8 = local_8 + 1) {
      if ((int)*(char *)(DAT_007a49f8 + 0x18 + local_8 * 4) == (param_1 & 0xff)) {
        *(undefined1 *)(DAT_007a49f8 + 0x18 + local_8 * 4) = (undefined1)param_2;
      }
    }
  }
  local_8 = 0x49744e;
  FUN__text__0056ce80();
  return;
}

