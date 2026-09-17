
void FUN__text__0049a9b0(undefined2 param_1,undefined2 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = param_4;
  if (param_4 == 0) {
    local_c = 0xff808080;
  }
  else if (param_4 == 4) {
    local_c = 0xff802020;
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlStMem.cpp",
                                DAT_0061a070 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__00495fe0(param_1,param_2,0xc5,param_3,0xff,param_4,local_c);
  local_8 = 0x49aa55;
  FUN__text__0056ce80();
  return;
}

