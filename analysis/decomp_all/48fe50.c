
void FUN__text__0048fe50(undefined4 param_1,byte *param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_4 == 0) &&
     (iVar2 = FUN__text__00424f80("cno != 0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp"
                                  ,DAT_006191e8 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*param_2 != 0) {
    if (((*param_2 == 0) || (0x45 < *param_2)) &&
       (iVar2 = FUN__text__00424f80("(1<=cond_now->type)&&(cond_now->type<=(69))",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                    DAT_006191e8 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = &DAT_006f4088 + (uint)*param_2 * 0x10;
    if (((param_4 < 1) || (0x45 < param_4)) &&
       (iVar2 = FUN__text__00424f80("(1<=cno)&&(cno<=(69))",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                    DAT_006191e8 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = &DAT_006f4088 + param_4 * 0x10;
  }
  local_8 = 0x48ff64;
  FUN__text__0056ce80();
  return;
}

