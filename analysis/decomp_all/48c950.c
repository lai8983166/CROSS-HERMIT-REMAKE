
void FUN__text__0048c950(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  uint local_18;
  int local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = &DAT_006c2dc8 + param_1 * 0x48;
  local_18 = (uint)(byte)(&DAT_006c2de1)[param_1 * 0x48];
  switch(local_18) {
  case 0:
    iVar2 = FUN__text__00424f80(&DAT_0059e2c8,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f80 + 0xe,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
    break;
  case 2:
    iVar2 = FUN__text__0046af50(param_2,param_3);
    if (iVar2 != 1) goto LAB__text__0048caa6;
    break;
  case 3:
    local_14 = FUN__text__0046af50(param_2,param_3);
    if ((local_14 != 0) && (local_14 != 4)) goto LAB__text__0048caa6;
    break;
  case 4:
    if (*(short *)(param_2 + 2) != *(short *)(param_3 + 2)) goto LAB__text__0048caa6;
    break;
  case 5:
    if (*(short *)(param_2 + 2) == *(short *)(param_3 + 2)) goto LAB__text__0048caa6;
  }
  iVar2 = FUN__text__004695d0(param_3);
  if ((iVar2 == 0) && (local_1c = param_1, param_1 == 0x2b)) {
    local_10 = &DAT_006b2d88 + (uint)*(ushort *)(*(int *)(param_3 + 600) + 0xc) * 0x40;
  }
LAB__text__0048caa6:
  local_8 = 0x48cab3;
  FUN__text__0056ce80();
  return;
}

