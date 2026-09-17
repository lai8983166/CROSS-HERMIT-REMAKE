
void __fastcall FUN__text__00434850(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  short local_30;
  short local_2c;
  short local_28;
  short local_24;
  short local_20;
  int local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0xc258c;
  local_8 = param_1;
  iVar2 = FUN__text__004e2720(3,0);
  if ((iVar2 == 0) && (iVar2 = FUN__text__00469170(local_c), iVar2 != 0)) {
    uVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent017.cpp",
                                DAT_005ff7f4 + 0x11);
    uVar1 = uVar1 & 0x80000003;
    if ((int)uVar1 < 0) {
      uVar1 = (uVar1 - 1 | 0xfffffffc) + 1;
    }
    local_30 = (short)uVar1;
    local_20 = (short)(char)(&DAT_005ff7d4)[local_30 * 4];
    local_24 = (short)(char)(&DAT_005ff7d5)[local_30 * 4];
    local_28 = (short)(char)(&DAT_005ff7d6)[local_30 * 4];
    local_2c = (short)(char)(&DAT_005ff7d7)[local_30 * 4];
    FUN__text__0047fc60(0xe,(int)local_20,(int)local_24,(int)local_28);
    FUN__text__00498db0(0xe,2,(int)local_2c);
    FUN__text__00498db0(0xe,1,0);
    FUN__text__00498db0(0xe,3,1);
    FUN__text__004e29a0(3,0,1);
  }
  local_c = local_8 + 0xc206c;
  iVar2 = FUN__text__004e2720(3,1);
  if ((iVar2 == 0) && (iVar2 = FUN__text__00469170(local_c), iVar2 != 0)) {
    uVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent017.cpp",
                                DAT_005ff7f4 + 0x23);
    uVar1 = uVar1 & 0x80000003;
    if ((int)uVar1 < 0) {
      uVar1 = (uVar1 - 1 | 0xfffffffc) + 1;
    }
    local_30 = (short)uVar1;
    local_20 = (short)(char)(&DAT_005ff7d4)[local_30 * 4];
    local_24 = (short)(char)(&DAT_005ff7d5)[local_30 * 4];
    local_28 = (short)(char)(&DAT_005ff7d6)[local_30 * 4];
    local_2c = (short)(char)(&DAT_005ff7d7)[local_30 * 4];
    FUN__text__0047fc60(0xf,(int)local_20,(int)local_24,(int)local_28);
    FUN__text__00498db0(0xf,2,(int)local_2c);
    FUN__text__00498db0(0xf,1,0);
    FUN__text__00498db0(0xf,3,1);
    FUN__text__004e29a0(3,1,1);
  }
  iVar2 = FUN__text__00430c90(1,0);
  if (0 < iVar2) {
    if (*(int *)(local_8 + 0x2e6f8) < 54000) {
      FUN__text__00454bb0(1,0,0xe);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      goto LAB__text__00434c26;
    }
    local_10 = (uint)(*(short *)(local_8 + 0x115cce) == *(short *)(local_8 + 0x115cd6));
    local_14 = (uint)(*(short *)(local_8 + 0x115cd8) == *(short *)(local_8 + 0x115ce0));
    local_18 = (uint)(*(short *)(local_8 + 0x115ce8) == *(short *)(local_8 + 0x115cea));
    local_1c = FUN__text__00430ba0();
    if ((((local_10 == 0) || (local_14 == 0)) || (local_18 == 0)) || (local_1c == 0)) {
      if (((local_10 == 0) || (local_14 == 0)) || (local_18 == 0)) {
        if (((local_10 == 0) && (local_14 == 0)) && (local_18 == 0)) {
          FUN__text__00454bb0(1,0,0xb);
          *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
        }
        else {
          FUN__text__00454bb0(1,0,8);
          *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
        }
      }
      else {
        FUN__text__00454bb0(1,0,5);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
      }
    }
    else {
      FUN__text__00454bb0(1,0,2);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
    }
  }
  iVar2 = FUN__text__00430df0();
  if (iVar2 != 0) {
    FUN__text__00454bb0(1,0,0xe);
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
  }
LAB__text__00434c26:
  local_8 = 0x434c33;
  FUN__text__0056ce80();
  return;
}

