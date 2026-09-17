
void __thiscall
FUN__text__00466640(int param_1,int param_2,short param_3,short param_4,undefined4 param_5,
                   undefined4 param_6,undefined1 param_7,int param_8)

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
  local_c = param_1 + 0x10c680;
  local_8 = param_1;
  if (((param_2 < 0) || (9 < param_2)) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059c378,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b20 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (((param_8 < 0) || (0xf9 < param_8)) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059c340,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b20 + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x10c680 + param_2 * 0x520;
  FUN__text__00466780(param_2);
  *(int *)(local_c + 0x2ec) = (int)param_3 << 0x10;
  *(int *)(local_c + 0x2f0) = (int)param_4 << 0x10;
  if (param_2 < 5) {
    *(undefined2 *)(local_c + 0xc) = 0x370;
  }
  else if (param_2 < 10) {
    *(undefined2 *)(local_c + 0xc) = 100;
  }
  *(undefined1 *)(local_c + 5) = param_7;
  *(undefined2 *)(local_c + 0xe) = (undefined2)param_8;
  FUN__text__0046be50(local_c,param_5,0,0);
  local_8 = 0x466774;
  FUN__text__0056ce80();
  return;
}

