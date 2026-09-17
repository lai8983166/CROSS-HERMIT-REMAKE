
void __thiscall FUN__text__00481ef0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (undefined1 *)(param_1 + 0x115cac);
  local_8 = param_1;
  _memset(local_c,0,0xc);
  *local_c = (undefined1)param_2;
  local_10 = param_2;
  if (param_2 == 1) {
    *(undefined2 *)(local_c + 2) = 0;
    *(undefined2 *)(local_c + 4) = 0;
    *(undefined2 *)(local_c + 6) = 1;
  }
  else if (param_2 == 2) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                DAT_00618edc + 0x13,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *(undefined2 *)(local_c + 2) = 0;
    *(undefined2 *)(local_c + 4) = 0;
    *(undefined2 *)(local_c + 6) = 1;
  }
  local_8 = 0x481fb6;
  FUN__text__0056ce80();
  return;
}

