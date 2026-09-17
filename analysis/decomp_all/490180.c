
void FUN__text__00490180(int param_1,int param_2,int param_3,undefined4 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined1 *local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((param_2 < 0) || (3 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=kind)&&(kind<=3)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                  DAT_006191f4 + 0x4b,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((0x45 < param_3) &&
     (iVar2 = FUN__text__00424f80("cno<=(69)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                  DAT_006191f4 + 0x4c,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (undefined1 *)(param_1 + 0x14 + param_2 * 0x10);
  iVar2 = FUN__text__0048ff70(param_1,local_c,param_3);
  if (((iVar2 == 0) && (iVar2 = FUN__text__0048fe50(param_1,local_c,param_4,param_3), iVar2 != 0))
     && (FUN__text__004902e0(param_1,local_c,param_2), *(int *)(&DAT_00618fb8 + param_3 * 4) != 0))
  {
    *local_c = (undefined1)param_3;
    (**(code **)(&DAT_00618fb8 + param_3 * 4))(local_8,local_c,param_1,param_4);
    FUN__text__0056ce80();
  }
  local_8 = 0x490299;
  FUN__text__0056ce80();
  return;
}

