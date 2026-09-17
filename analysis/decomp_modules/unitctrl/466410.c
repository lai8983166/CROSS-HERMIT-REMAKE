
void __thiscall FUN__text__00466410(int param_1,int param_2,int *param_3,int *param_4)

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
  local_8 = param_1;
  if (((param_2 < 0) || (0xf9 < param_2)) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059c2e4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b1c + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x80aec + param_2 * 0x520;
  iVar2 = FUN__text__00468d10(local_c);
  if (iVar2 == 0) {
    iVar2 = FUN__text__00424f80(&DAT_0059c2bc,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b1c + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *param_3 = *(int *)(local_c + 0x2ec) >> 0x10;
    *param_4 = *(int *)(local_c + 0x2f0) >> 0x10;
  }
  local_8 = 0x4664ed;
  FUN__text__0056ce80();
  return;
}

