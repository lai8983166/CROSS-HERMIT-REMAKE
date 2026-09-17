
void FUN__text__00432b70(void)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  uint local_34;
  uint local_30;
  int local_2c;
  int local_28;
  undefined4 local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = 10;
  iVar2 = FUN__text__004e2720(3,9);
  if (iVar2 == 0) {
    local_1c = 0;
    for (local_18 = 0; local_18 != 3; local_18 = local_18 + 1) {
      local_c = local_8 + 0x80aec + (0xf9 - ((char)(&DAT_005ff754)[local_18] + -1)) * 0x520;
      iVar2 = FUN__text__00469480(local_c);
      if ((iVar2 != 0) && (*(short *)(*(int *)(local_c + 600) + 0x16) < 200)) {
        FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
        FUN__text__00454bb0(0,0,0x1d);
        FUN__text__004e29a0(3,9,1);
        goto LAB__text__00433029;
      }
    }
  }
  local_10 = local_8 + 0xcf28c;
  local_14 = local_8 + 0xced6c;
  local_28 = FUN__text__0046a430(local_10);
  local_2c = FUN__text__0046a430(local_14);
  if ((local_28 == 1) && (local_2c == 1)) {
    FUN__text__004e29a0(2,0,1);
  }
  else {
    FUN__text__004e29a0(2,0,0);
  }
  local_1c = 0;
  for (local_18 = 0; local_18 != 3; local_18 = local_18 + 1) {
    local_c = local_8 + 0x80aec + (0xf9 - ((char)(&DAT_005ff754)[local_18] + -1)) * 0x520;
    iVar2 = FUN__text__004690a0(local_c);
    if ((iVar2 != 0) && (iVar2 = FUN__text__004695d0(local_c), iVar2 != 0)) {
      local_1c = local_1c + 1;
    }
  }
  if (((local_1c == 0) || (iVar2 = FUN__text__004e2720(3,0), iVar2 == 0)) ||
     (iVar2 = FUN__text__004551c0(0,0x18), iVar2 == 0)) {
    iVar2 = FUN__text__004e2720(3,2);
    if (iVar2 == 0) {
      local_c = local_8 + 0xcf7ac;
      iVar2 = FUN__text__0046a430(local_c);
      if ((iVar2 != 0) && (iVar2 = FUN__text__004551c0(0,0x19), iVar2 != 0)) {
        FUN__text__004549d0(0,0,0x19,0,0,1,1);
        goto LAB__text__00433029;
      }
    }
    iVar2 = FUN__text__004e2720(3,3);
    if ((iVar2 == 0) && ((local_28 != 0 || (local_2c != 0)))) {
      iVar2 = FUN__text__0046a430(local_10);
      if (iVar2 == 0) {
        sVar1 = *(short *)(local_14 + 2);
      }
      else {
        sVar1 = *(short *)(local_10 + 2);
      }
      local_20 = (int)sVar1;
      FUN__text__004e29a0(1,0,local_20);
      iVar2 = FUN__text__004551c0(0,0x1a);
      if (iVar2 != 0) {
        FUN__text__004549d0(0,0,0x1a,0,0,1,1);
        goto LAB__text__00433029;
      }
    }
    iVar2 = FUN__text__00430df0();
    if (iVar2 == 0) {
      iVar2 = FUN__text__004e2720(3,7);
      if ((iVar2 != 0) && (iVar2 = FUN__text__00430d40(), iVar2 == 0)) {
        iVar2 = FUN__text__004e2720(2,1);
        if (iVar2 == 0) {
          local_30 = (uint)(*(short *)(local_8 + 0x115cce) == *(short *)(local_8 + 0x115cd6));
          local_34 = (uint)(*(short *)(local_8 + 0x115ce2) == *(short *)(local_8 + 0x115cea));
          iVar2 = FUN__text__00430ba0();
          if (((iVar2 == 0) || (local_30 == 0)) || (local_34 == 0)) {
            if ((local_30 == 0) || (local_34 == 0)) {
              FUN__text__00454bb0(1,0,0xb);
              *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
            }
            else {
              FUN__text__00454bb0(1,0,8);
              *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
            }
          }
          else {
            FUN__text__00454bb0(1,0,2);
            *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
          }
        }
        else {
          FUN__text__00454bb0(1,0,0xb);
          *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
        }
      }
    }
    else {
      iVar2 = FUN__text__004551c0(0,0xe);
      if (iVar2 != 0) {
        FUN__text__004549d0(0,0,0xe,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      }
    }
  }
  else {
    FUN__text__004549d0(0,0,0x18,0,0,1,1);
    FUN__text__004e29e0(0xffffffff,3,0,0);
    FUN__text__004e29e0(0xffffffff,3,1,0);
  }
LAB__text__00433029:
  local_8 = 0x433036;
  FUN__text__0056ce80();
  return;
}

