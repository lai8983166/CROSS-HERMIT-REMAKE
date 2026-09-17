
void __thiscall
FUN__text__0043c1d0(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined4 local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x2659c) != 0) {
    local_8 = param_1;
    if (((param_6 < 0) || (0x20 < param_6)) &&
       (iVar2 = FUN__text__00424f80("(0<=view)&&(view<=32)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9f8 + 6,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = (int)(char)(&DAT_0059558c)[param_6 * 2];
    local_18 = (int)(char)(&DAT_0059558d)[param_6 * 2];
    iVar2 = FUN__text__0056db00(param_2 - param_4);
    if ((iVar2 <= (local_14 + -1) / 2) &&
       (iVar2 = FUN__text__0056db00(param_3 - param_5), iVar2 <= (local_18 + -1) / 2)) {
      local_1c = *(undefined4 *)(local_8 + 8 + param_6 * 4);
      local_c = FUN__text__0056db00(param_2 - param_4);
      local_c = local_c + (local_14 + -1) / 2;
      local_10 = FUN__text__0056db00(param_3 - param_5);
      local_10 = local_10 + (local_18 + -1) / 2;
    }
  }
  local_8 = 0x43c312;
  FUN__text__0056ce80();
  return;
}

