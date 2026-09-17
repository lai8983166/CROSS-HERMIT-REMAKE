
void FUN__text__0046d970(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if (iVar2 == 0) {
    iVar2 = FUN__text__00424f80("IsUwUsed(wk)","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618c24 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  iVar2 = FUN__text__0046a4c0(param_1);
  if (iVar2 == 0) {
    iVar2 = FUN__text__00424f80("IsUwPlayerStudent(wk)",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",DAT_00618c24 + 2
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (0x14 < *(int *)(local_8 + 0xdb814)) {
    iVar2 = FUN__text__00424f80("FaceCnt <= 20","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618c24 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined1 *)(param_1 + 0x501) = *(undefined1 *)(local_8 + 0xdb814);
  *(int *)(local_8 + 0xdb818 + *(int *)(local_8 + 0xdb814) * 4) = param_1;
  *(int *)(local_8 + 0xdb814) = *(int *)(local_8 + 0xdb814) + 1;
  local_8 = 0x46da6f;
  FUN__text__0056ce80();
  return;
}

