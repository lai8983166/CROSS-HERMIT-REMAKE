
void __thiscall FUN__text__0044ed40(int param_1,undefined4 *param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_b4 [16];
  byte *local_74;
  int local_70;
  byte *local_6c;
  int local_68;
  int local_64;
  byte *local_60;
  int local_5c;
  int local_58;
  ushort local_54;
  ushort local_50;
  int local_4c;
  undefined4 local_48;
  int local_44;
  int local_40;
  int local_3c;
  ushort local_36;
  ushort local_34;
  int local_20;
  int local_1c;
  undefined1 *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_b4;
  for (iVar1 = 0x2c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_48 = 0;
  local_4c = 0;
  local_10 = 0;
  local_5c = (int)*(short *)(param_2 + 8);
  local_8 = param_1;
  local_60 = (byte *)FUN__text__0044e650(*(undefined4 *)(param_1 + 0xc),local_5c);
  local_50 = (ushort)*local_60;
  local_54 = (ushort)local_60[1];
  do {
    iVar1 = FUN__text__004399c0();
    if (iVar1 == 0) {
LAB__text__0044f14a:
      if (local_10 == 1) {
        FUN__text__0044f1e0(local_18,param_2,param_3);
        FUN__text__00439750(local_14);
      }
      else {
        *(undefined2 *)((int)param_2 + 0x1e) = 0;
        *(undefined2 *)(param_2 + 8) = 0;
      }
      FUN__text__00439c60();
      *param_2 = *(undefined4 *)(local_8 + 0x54);
      param_2[1] = *(undefined4 *)(local_8 + 0x58);
      param_2[2] = *(undefined4 *)(local_8 + 0x5c);
      param_2[3] = *(undefined4 *)(local_8 + 0x60);
      param_2[4] = *(undefined4 *)(local_8 + 100);
      param_2[5] = *(undefined4 *)(local_8 + 0x68);
      local_8 = 0x44f1da;
      FUN__text__0056ce80();
      return;
    }
    local_14 = FUN__text__00439c20();
    local_18 = *(undefined1 **)(local_14 + 8);
    local_1c = *(int *)(local_18 + 0x14);
    local_58 = *(int *)(local_18 + 0x18);
    if (local_58 == local_5c) {
      local_10 = 1;
      goto LAB__text__0044f14a;
    }
    local_64 = FUN__text__0044e650(*(undefined4 *)(local_8 + 0xc),local_58);
    for (local_c = 0; local_c != *(short *)(local_64 + 2); local_c = local_c + 1) {
      local_68 = local_64 + 4 + local_c * 0xc;
      local_6c = (byte *)FUN__text__0044e650(*(undefined4 *)(local_8 + 0xc),
                                             (int)*(short *)(local_64 + 4 + local_c * 0xc));
      local_36 = (ushort)*local_6c;
      local_34 = (ushort)local_6c[1];
      local_20 = (int)*(short *)(local_64 + 4 + local_c * 0xc);
      local_44 = *(int *)(local_64 + 0xc + local_c * 0xc);
      if (((((*(ushort *)(local_18 + 2) != local_36) || (*(ushort *)(local_18 + 4) != local_34)) &&
           ((local_1c == 0 ||
            ((*(ushort *)(local_1c + 2) != local_36 || (*(ushort *)(local_1c + 4) != local_34))))))
          && (-1 < (short)local_36)) &&
         ((((int)(short)local_36 < *(int *)(local_8 + 0x40) && (-1 < (short)local_34)) &&
          ((int)(short)local_34 < *(int *)(local_8 + 0x44))))) {
        local_3c = *(int *)(local_18 + 8) + local_44;
        local_40 = ((int)(short)local_34 - (int)(short)local_54) *
                   ((int)(short)local_34 - (int)(short)local_54) + local_3c +
                   ((int)(short)local_36 - (int)(short)local_50) *
                   ((int)(short)local_36 - (int)(short)local_50);
        local_70 = FUN__text__00439820(local_36,local_34);
        if (local_70 == 0) {
          local_70 = FUN__text__004396e0();
          local_74 = *(byte **)(local_70 + 8);
          *local_74 = 0x40;
          *(ushort *)(local_74 + 2) = local_36;
          *(ushort *)(local_74 + 4) = local_34;
          *(undefined1 **)(local_74 + 0x14) = local_18;
          *(int *)(local_74 + 8) = local_3c;
          *(int *)(local_74 + 0xc) =
               ((int)(short)local_36 - (int)(short)local_50) *
               ((int)(short)local_36 - (int)(short)local_50) +
               ((int)(short)local_34 - (int)(short)local_54) *
               ((int)(short)local_34 - (int)(short)local_54);
          *(int *)(local_74 + 0x10) = *(int *)(local_74 + 8) + *(int *)(local_74 + 0xc);
          *(int *)(local_74 + 0x18) = local_20;
          FUN__text__00439a90(local_70);
          FUN__text__004398d0((int)(short)local_36,(int)(short)local_34,local_70);
        }
        else {
          local_74 = *(byte **)(local_70 + 8);
          if ((*local_74 & 0x40) == 0) {
            if (local_3c < *(int *)(local_74 + 8)) {
              FUN__text__00427d20(local_70);
              *(undefined1 **)(local_74 + 0x14) = local_18;
              *(int *)(local_74 + 8) = local_3c;
              *(int *)(local_74 + 0x10) = *(int *)(local_74 + 8) + *(int *)(local_74 + 0xc);
              goto LAB__text__0044f0ee;
            }
          }
          else if (local_3c < *(int *)(local_74 + 8)) {
            FUN__text__00427c90(local_70);
            *(undefined1 **)(local_74 + 0x14) = local_18;
            *(int *)(local_74 + 8) = local_3c;
            *(int *)(local_74 + 0x10) = *(int *)(local_74 + 8) + *(int *)(local_74 + 0xc);
LAB__text__0044f0ee:
            *local_74 = 0x40;
            FUN__text__00439a90(local_70);
          }
        }
      }
    }
    *local_18 = 0x80;
    FUN__text__00439ae0(local_14);
    FUN__text__004398d0((int)*(short *)(local_18 + 2),(int)*(short *)(local_18 + 4),local_14);
    local_4c = local_4c + 1;
  } while( true );
}

