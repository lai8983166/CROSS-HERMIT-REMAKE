
void __thiscall FUN__text__0043bb90(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined1 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < 0) &&
     (iVar2 = FUN__text__00424f80("0 <= cx","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9e8 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((param_3 < 0) &&
     (iVar2 = FUN__text__00424f80("0 <= cy","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9e8 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(short *)(*(int *)(local_8 + 0x2659c) + 4) <= param_2) &&
     (iVar2 = FUN__text__00424f80("cx < MapCw->cellw",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9e8 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(short *)(*(int *)(local_8 + 0x2659c) + 6) <= param_3) &&
     (iVar2 = FUN__text__00424f80("cy < MapCw->cellh",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9e8 + 8,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((((-1 < param_2) && (-1 < param_3)) && (param_2 < *(short *)(*(int *)(local_8 + 0x2659c) + 4))
      ) && (param_3 < *(short *)(*(int *)(local_8 + 0x2659c) + 6))) {
    local_c = param_3 * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + param_2;
    local_10 = *(undefined1 *)(*(int *)(local_8 + 0x2659c) + 0x12 + local_c * 6);
  }
  local_8 = 0x43bcf1;
  FUN__text__0056ce80();
  return;
}

