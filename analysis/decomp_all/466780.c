
void __thiscall FUN__text__00466780(int param_1,int param_2)

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
     (iVar2 = FUN__text__00424f80(&DAT_0059c3c8,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b24 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x10c680 + param_2 * 0x520;
  FUN__text__0040ad20(local_c + 0x48);
  local_8 = 0x466819;
  FUN__text__0056ce80();
  return;
}

