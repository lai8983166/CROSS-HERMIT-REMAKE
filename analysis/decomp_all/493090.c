
void FUN__text__00493090(undefined4 param_1,short param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00492f40();
  if (local_c == 0) {
    iVar2 = FUN__text__00424f80("dw!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                DAT_00619268 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined1 *)(local_c + 1) = 0;
  *(short *)(local_c + 2) = param_2;
  FUN__text__00493020(param_1,local_c);
  if (param_2 < 1) {
    if (param_3 == 0) {
      local_10 = 0;
    }
    else if (param_3 == 1) {
      local_10 = 1;
    }
  }
  else {
    local_10 = 2;
  }
  iVar2 = FUN__text__0046a430(param_1);
  if (iVar2 == 0) {
    local_10 = local_10 + 9;
  }
  FUN__text__00494e70(param_1,(int)param_2,local_10);
  local_8 = 0x49316c;
  FUN__text__0056ce80();
  return;
}

