
void FUN__text__00434060(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = FUN__text__00451d10();
  iVar2 = FUN__text__004e2760(0xffffffff,3,0);
  if (iVar2 == 0) {
    local_c = local_8 + 0xce84c;
    iVar2 = FUN__text__00469170(local_c);
    if (iVar2 != 0) {
      iVar2 = FUN__text__004551c0(0,0x1b);
      if ((iVar2 != 0) &&
         (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent011.cpp",
                                      DAT_005ff7ac + 10,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__004342d6;
    }
  }
  if (*(int *)(local_8 + 0x2e6f4) == 0) {
    local_18 = FUN__text__004e2760(0xffffffff,2,0);
    local_10 = local_18;
    switch(local_18) {
    case 0:
      iVar2 = FUN__text__004551c0(0,2);
      if (iVar2 != 0) {
        FUN__text__004549d0(0,0,2,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
      }
      break;
    case 1:
    case 2:
    case 3:
      iVar2 = FUN__text__004551c0(0,5);
      if (iVar2 != 0) {
        FUN__text__004549d0(0,0,5,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
      }
      break;
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
      iVar2 = FUN__text__004551c0(0,8);
      if (iVar2 != 0) {
        FUN__text__004549d0(0,0,8,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
      }
    }
  }
  local_10 = FUN__text__004e2760(0xffffffff,2,0);
  if (local_10 < 10) {
    iVar2 = FUN__text__00430df0();
    if ((iVar2 != 0) && (iVar2 = FUN__text__004551c0(0,0xe), iVar2 != 0)) {
      FUN__text__004549d0(0,0,0xe,1,0,1,1);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
    }
  }
  else {
    iVar2 = FUN__text__004551c0(0,0xb);
    if (iVar2 != 0) {
      FUN__text__004549d0(0,0,0xb,1,0,1,1);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
    }
  }
LAB__text__004342d6:
  local_8 = 0x4342e3;
  FUN__text__0056ce80();
  return;
}

