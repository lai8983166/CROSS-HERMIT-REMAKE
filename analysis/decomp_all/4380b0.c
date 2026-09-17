
void __thiscall FUN__text__004380b0(int param_1,undefined4 *param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_9c [16];
  byte *local_5c;
  int local_58;
  short local_54;
  short local_50;
  int local_4c;
  undefined4 local_48;
  int local_44;
  int local_40;
  int local_3c;
  short local_36;
  short local_34;
  int local_1c;
  undefined1 *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_48 = 0;
  local_4c = 0;
  local_10 = 0;
  local_50 = *(short *)(param_2 + 6);
  local_54 = *(short *)((int)param_2 + 0x1a);
  local_8 = param_1;
  do {
    iVar1 = FUN__text__004399c0();
    if (iVar1 == 0) {
LAB__text__004384e8:
      if (local_10 == 1) {
        FUN__text__00438610(local_18,param_2,param_3);
        FUN__text__00439750(local_14);
      }
      else {
        *(undefined2 *)((int)param_2 + 0x1e) = 0;
        *(undefined2 *)(param_2 + 8) = 0;
      }
      FUN__text__00439c60();
      goto LAB__text__00438530;
    }
    local_14 = FUN__text__00439c20();
    local_18 = *(undefined1 **)(local_14 + 8);
    local_1c = *(int *)(local_18 + 0x14);
    if ((*(short *)(local_18 + 2) == local_50) && (*(short *)(local_18 + 4) == local_54)) {
      local_10 = 1;
      goto LAB__text__004384e8;
    }
    for (local_c = 0; local_c != 8; local_c = local_c + 1) {
      local_36 = *(short *)(local_18 + 2) + *(short *)(&DAT_005ff910 + local_c * 8);
      local_34 = *(short *)(local_18 + 4) + *(short *)(&DAT_005ff912 + local_c * 8);
      local_44 = *(int *)(&DAT_005ff914 + local_c * 8);
      if (((((*(short *)(local_18 + 2) != local_36) || (*(short *)(local_18 + 4) != local_34)) &&
           ((local_1c == 0 ||
            ((*(short *)(local_1c + 2) != local_36 || (*(short *)(local_1c + 4) != local_34)))))) &&
          (-1 < local_36)) &&
         ((((int)local_36 < *(int *)(local_8 + 0x48) && (-1 < local_34)) &&
          ((int)local_34 < *(int *)(local_8 + 0x4c))))) {
        if ((local_36 != local_50) || (local_34 != local_54)) {
          iVar1 = FUN__text__0043bfa0((int)local_36,(int)local_34,*(undefined4 *)(local_8 + 0x14));
          if (iVar1 == 0) {
            local_44 = DAT_005ff908 * DAT_005ff908;
          }
          if ((param_3 != 0) &&
             (iVar1 = FUN__text__0043c0c0((int)local_36,(int)local_34), iVar1 != 0)) {
            local_44 = 100;
          }
        }
        local_3c = *(int *)(local_18 + 8) + local_44;
        local_40 = ((int)local_34 - (int)local_54) * ((int)local_34 - (int)local_54) + local_3c +
                   ((int)local_36 - (int)local_50) * ((int)local_36 - (int)local_50);
        local_58 = FUN__text__00439820((int)local_36,(int)local_34);
        if (local_58 == 0) {
          local_58 = FUN__text__004396e0();
          local_5c = *(byte **)(local_58 + 8);
          *local_5c = 0x40;
          *(short *)(local_5c + 2) = local_36;
          *(short *)(local_5c + 4) = local_34;
          *(undefined1 **)(local_5c + 0x14) = local_18;
          *(int *)(local_5c + 8) = local_3c;
          *(int *)(local_5c + 0xc) =
               ((int)local_36 - (int)local_50) * ((int)local_36 - (int)local_50) +
               ((int)local_34 - (int)local_54) * ((int)local_34 - (int)local_54);
          *(int *)(local_5c + 0x10) = *(int *)(local_5c + 8) + *(int *)(local_5c + 0xc);
          FUN__text__00439a90(local_58);
          FUN__text__004398d0((int)local_36,(int)local_34,local_58);
        }
        else {
          local_5c = *(byte **)(local_58 + 8);
          if ((*local_5c & 0x40) == 0) {
            if (local_3c < *(int *)(local_5c + 8)) {
              FUN__text__00427d20(local_58);
              *(undefined1 **)(local_5c + 0x14) = local_18;
              *(int *)(local_5c + 8) = local_3c;
              *(int *)(local_5c + 0x10) = *(int *)(local_5c + 8) + *(int *)(local_5c + 0xc);
              goto LAB__text__00438477;
            }
          }
          else if (local_3c < *(int *)(local_5c + 8)) {
            FUN__text__00427c90(local_58);
            *(undefined1 **)(local_5c + 0x14) = local_18;
            *(int *)(local_5c + 8) = local_3c;
            *(int *)(local_5c + 0x10) = *(int *)(local_5c + 8) + *(int *)(local_5c + 0xc);
LAB__text__00438477:
            *local_5c = 0x40;
            FUN__text__00439a90(local_58);
          }
        }
      }
    }
    *local_18 = 0x80;
    FUN__text__00439ae0(local_14);
    FUN__text__004398d0((int)*(short *)(local_18 + 2),(int)*(short *)(local_18 + 4),local_14);
    local_4c = local_4c + 1;
  } while (local_4c < 0x3e9);
  local_10 = -1;
LAB__text__00438530:
  *param_2 = *(undefined4 *)(local_8 + 0x5c);
  param_2[1] = *(undefined4 *)(local_8 + 0x60);
  param_2[2] = *(undefined4 *)(local_8 + 100);
  param_2[3] = *(undefined4 *)(local_8 + 0x68);
  param_2[4] = *(undefined4 *)(local_8 + 0x6c);
  param_2[5] = *(undefined4 *)(local_8 + 0x70);
  *(short *)(param_2 + 6) = local_50;
  *(short *)((int)param_2 + 0x1a) = local_54;
  local_8 = 0x438592;
  FUN__text__0056ce80();
  return;
}

