
void FUN__text__0046a120(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwUsed(wk)!=0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618bbc + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  iVar2 = FUN__text__004695d0(param_1);
  if (iVar2 != 0) {
    local_c = (uint)*(byte *)(*(int *)(param_1 + 600) + 0xf);
    switch(local_c) {
    case 0:
    case 2:
      iVar2 = FUN__text__00469ad0(param_1);
      if ((iVar2 == 0) && (iVar2 = FUN__text__00469c60(param_1), iVar2 == 0)) {
        FUN__text__00469b90(param_1);
      }
      break;
    case 1:
    case 3:
    case 4:
    case 5:
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618bbc + 0x14,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = 0x46a22a;
  FUN__text__0056ce80();
  return;
}

