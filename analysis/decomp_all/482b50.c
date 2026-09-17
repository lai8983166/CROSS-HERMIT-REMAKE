
void __thiscall FUN__text__00482b50(int param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((0xf9 < *(byte *)(param_4 + 2)) &&
     (iVar2 = FUN__text__00424f80("(0<=data->from) && (data->from<(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f04 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((0xf9 < *(byte *)(param_4 + 3)) &&
     (iVar2 = FUN__text__00424f80("(0<=data->to ) && (data->to <(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f04 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x80aec + (uint)*(byte *)(param_4 + 2) * 0x520;
  local_10 = local_8 + 0x80aec + (uint)*(byte *)(param_4 + 3) * 0x520;
  local_14 = &DAT_006c2dc8 + *(short *)(param_4 + 4) * 0x48;
  iVar2 = FUN__text__00468d10(local_c);
  if (((iVar2 != 0) && (iVar2 = FUN__text__004690a0(local_c), iVar2 != 0)) ||
     ((iVar2 = FUN__text__00468d10(local_10), iVar2 != 0 &&
      (iVar2 = FUN__text__004690a0(local_10), iVar2 != 0)))) goto LAB__text__00482d11;
  local_18 = (int)*(short *)(param_4 + 4);
  if (local_18 < 0x83) {
    if (local_18 < 0x65) {
      if ((0 < local_18) && (local_18 < 100)) {
        FUN__text__00488bc0(local_c,local_10,param_4);
        goto LAB__text__00482d11;
      }
LAB__text__00482cf4:
      FUN__text__0048aae0(local_c,local_10,param_4,local_14);
      goto LAB__text__00482d11;
    }
  }
  else if ((local_18 < 0x1ed) || (0x1f2 < local_18)) goto LAB__text__00482cf4;
  FUN__text__0048aae0(local_c,local_10,param_4,local_14);
LAB__text__00482d11:
  local_8 = 0x482d1e;
  FUN__text__0056ce80();
  return;
}

