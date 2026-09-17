
void FUN__text__00475270(int param_1,undefined1 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  char local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  *(undefined1 *)(param_1 + 0x292) = param_2;
  local_10 = *(char *)(param_1 + 0x292);
  if (local_10 == '\0') {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618df0 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else if (local_10 == '\x06') {
    if ((*(short *)(param_1 + 0x4f2) == -1) &&
       (iVar2 = FUN__text__00424f80("wk->bomno!=-1",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618df0 + 9,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else if (((local_10 == '\x1d') && (*(short *)(param_1 + 0x4ee) == -1)) &&
          (iVar2 = FUN__text__00424f80("wk->target!=-1",
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                       DAT_00618df0 + 0xd,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x475365;
  FUN__text__0056ce80();
  return;
}

