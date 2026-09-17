
void __fastcall FUN__text__0049b180(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  undefined4 local_18;
  int local_14;
  short local_10;
  undefined2 local_c;
  int local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined1 *)(param_1 + 0x2f157) = 0;
  local_8 = param_1;
  if (*(char *)(param_1 + 0x108b48) != '\0') {
    FUN__text__0049b9f0();
    goto LAB__text__0049b68d;
  }
  if (*(char *)(param_1 + 0x108b3a) == '\0') goto LAB__text__0049b643;
  FUN__text__0049ba60();
  if (*(int *)(local_8 + 0x108b50) != 0) {
    local_1c = 0;
    local_20 = 0;
    iVar2 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0x108b60));
    if (iVar2 != 0) {
      for (local_14 = 0; local_14 != *(int *)(local_8 + 0x108b50); local_14 = local_14 + 1) {
        iVar2 = FUN__text__004690a0(*(undefined4 *)(local_8 + 0x108b60 + local_14 * 4));
        if (iVar2 == 0) {
          if (local_20 == 0) {
            local_20 = *(int *)(local_8 + 0x108b60 + local_14 * 4);
          }
          local_1c = local_1c + 1;
        }
      }
    }
    if (local_20 == 0) {
      local_20 = *(int *)(local_8 + 0x108b60);
    }
    iVar2 = FUN__text__0046a430(local_20);
    if (iVar2 != 0) {
      if (local_1c == 1) {
        iVar2 = FUN__text__00469480(local_20);
        if (iVar2 != 0) {
          local_30 = FUN__text__004128f0(0x2a,0);
          local_2c = FUN__text__004128f0(0x36,0);
          if ((local_30 == 0) && (local_2c == 0)) {
            local_30 = FUN__text__004128f0(0x2a,4);
            local_2c = FUN__text__004128f0(0x36,4);
            if ((local_30 != 0) || (local_2c != 0)) {
              *(undefined1 *)(*(int *)(local_20 + 600) + 0x9d) = 0;
            }
          }
          else {
            *(undefined1 *)(*(int *)(local_20 + 600) + 0x9d) = 1;
          }
        }
      }
      else {
        for (local_14 = 0; local_14 != *(int *)(local_8 + 0x108b50); local_14 = local_14 + 1) {
          iVar2 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0x108b60 + local_14 * 4));
          if ((iVar2 != 0) &&
             (iVar2 = FUN__text__00469480(*(undefined4 *)(local_8 + 0x108b60 + local_14 * 4)),
             iVar2 != 0)) {
            *(undefined1 *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_14 * 4) + 600) + 0x9d) = 0;
          }
        }
      }
    }
    _memset(&local_28,0,8);
    if ((local_1c == 1) && (iVar2 = FUN__text__004577f0(), iVar2 == 0)) {
      for (local_14 = 0; local_14 != 8; local_14 = local_14 + 1) {
        iVar2 = FUN__text__004128f0((&DAT_0061aea0)[local_14],1);
        if (iVar2 != 0) {
          local_28 = local_14 + 1;
          break;
        }
      }
    }
  }
  if ((*(int *)(local_8 + 0x108b50) == 0) ||
     (iVar2 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0x108b60)), iVar2 == 0)) {
LAB__text__0049b5c9:
    if (DAT_0061adcc <= local_10) {
      iVar2 = FUN__text__00470070(DAT_0061adc8,CONCAT22(local_10 >> 0xf,(undefined2)DAT_0061adcc),
                                  0x24,0x24,local_c,local_10);
      if (iVar2 != 0) {
        if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) {
          *(undefined1 *)(local_8 + 0x2f157) = 1;
        }
        if ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0) {
          FUN__text__0049bb20();
          FUN__text__0049ad50(3);
        }
        goto LAB__text__0049b652;
      }
    }
  }
  else {
    local_c = *(undefined2 *)(DAT_007a49fc + 0x196c);
    local_10 = *(short *)(DAT_007a49fc + 0x1970);
    if ((local_28 != 0) || (local_24 != 0)) {
      local_18 = 0;
LAB__text__0049b54c:
      local_3c = FUN__text__0049b6a0(local_20,local_1c,
                                     CONCAT22((short)((uint)&local_28 >> 0x10),local_c),local_10,
                                     local_18,&local_28);
      local_38 = local_3c;
      if (local_3c == 0) goto LAB__text__0049b5c9;
      if (local_3c == 1) goto LAB__text__0049b643;
      if (local_3c != 2) {
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061afec + 0xa8,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        goto LAB__text__0049b5c9;
      }
LAB__text__0049b652:
      *(undefined4 *)(local_8 + 0x2f150) = 1;
      goto LAB__text__0049b68d;
    }
    if ((599 < local_10) &&
       ((*(int *)(DAT_007a49fc + 0x19b8) == 0 || (599 < *(int *)(DAT_007a49fc + 0x19c0))))) {
      if ((local_1c == 1) && ((*(uint *)(DAT_007a49fc + 0x1990) & 8) != 0)) {
        local_34 = FUN__text__004128f0(0x2a,0);
        iVar2 = FUN__text__004128f0(0x36,0);
        local_34 = local_34 + iVar2;
        if (local_34 != 0) goto LAB__text__0049b643;
        local_18 = 1;
      }
      else {
        local_18 = 0;
        if ((*(uint *)(DAT_007a49fc + 0x199c) & 1) == 0) goto LAB__text__0049b5c9;
      }
      goto LAB__text__0049b54c;
    }
  }
LAB__text__0049b643:
  *(undefined4 *)(local_8 + 0x2f150) = 0;
LAB__text__0049b68d:
  local_8 = 0x49b69a;
  FUN__text__0056ce80();
  return;
}

