
void __thiscall
FUN__text__0049b6a0(int param_1,undefined4 param_2,int param_3,undefined2 param_4,short param_5,
                   int param_6,int *param_7)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*param_7 == 0) && (param_7[1] == 0)) {
    local_14 = param_6;
    if (param_6 != 1) {
      if ((param_6 == 2) &&
         (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                      DAT_0061aff0 + 0x17,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0049b793;
    }
  }
  else {
    if (*param_7 != 0) {
      local_c = *param_7 + -1;
LAB__text__0049b873:
      FUN__text__0049be60(param_2,local_c,param_6);
      goto LAB__text__0049b9dd;
    }
    if (param_7[1] == 0) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                  DAT_0061aff0 + 0xe,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                  DAT_0061aff0 + 0xc,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
LAB__text__0049b793:
    if ((int)DAT_0061add4 <= (int)param_5) {
      if ((param_5 < DAT_0061adc4) &&
         ((*(int *)(local_8 + 0x108b50) != 1 ||
          (iVar2 = FUN__text__00470070(DAT_0061add0,DAT_0061add4 & 0xffff,0x24,0x24,
                                       CONCAT22(param_5 >> 0xf,param_4),param_5), iVar2 == 0)))) {
        for (local_c = 0; local_c != 4; local_c = local_c + 1) {
          iVar2 = FUN__text__00470070(CONCAT22((short)((uint)local_c >> 0x10),
                                               *(undefined2 *)(&DAT_0061ae18 + local_c * 8)),
                                      *(undefined2 *)(&DAT_0061ae1c + local_c * 8),0x24,0x24,param_4
                                      ,param_5);
          if (iVar2 != 0) {
            FUN__text__0049bc90(0,local_c);
            FUN__text__0049ad50(0);
            goto LAB__text__0049b9dd;
          }
        }
        for (local_c = 0; local_c != 4; local_c = local_c + 1) {
          iVar2 = FUN__text__00470070(CONCAT22((short)((uint)local_c >> 0x10),
                                               *(undefined2 *)(&DAT_0061ae38 + local_c * 8)),
                                      *(undefined2 *)(&DAT_0061ae3c + local_c * 8),0x24,0x24,param_4
                                      ,param_5);
          if (iVar2 != 0) {
            FUN__text__0049bc90(1,local_c);
            FUN__text__0049ad50(0);
            break;
          }
        }
      }
      goto LAB__text__0049b9dd;
    }
    if (param_3 != 1) goto LAB__text__0049b9dd;
    local_10 = FUN__text__004128f0(0x2a,0);
    iVar2 = FUN__text__004128f0(0x36,0);
    local_10 = local_10 + iVar2;
    if ((local_10 == 0) &&
       (iVar2 = FUN__text__00470070(DAT_0061adb8,DAT_0061adbc,0x24,0x24,
                                    CONCAT22(extraout_var,param_4),param_5), iVar2 != 0)) {
      FUN__text__0049bc30(param_2,0);
      goto LAB__text__0049b9dd;
    }
  }
  for (local_c = 0; local_c != 8; local_c = local_c + 1) {
    iVar2 = FUN__text__00470070(CONCAT22((short)((uint)local_c >> 0x10),
                                         *(undefined2 *)(&DAT_0061add8 + local_c * 8)),
                                *(undefined2 *)(&DAT_0061addc + local_c * 8),0x24,0x24,param_4,
                                param_5);
    if (iVar2 != 0) goto LAB__text__0049b873;
  }
LAB__text__0049b9dd:
  local_8 = 0x49b9ea;
  FUN__text__0056ce80();
  return;
}

