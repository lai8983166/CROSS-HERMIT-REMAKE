
void __thiscall
FUN__text__00495fe0(int param_1,short param_2,short param_3,undefined2 param_4,int param_5,
                   undefined1 param_6,undefined4 param_7,undefined4 param_8)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_70 [16];
  undefined4 local_30;
  int local_2c;
  uint local_28;
  int local_24;
  int local_20;
  int local_1c;
  byte abStack_18 [12];
  short *local_c;
  int local_8;
  
  puVar4 = local_70;
  for (iVar3 = 0x1b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (999999 < param_5) {
    param_5 = 999999;
  }
  if (param_5 < 0) {
    param_5 = 0;
  }
  local_20 = 1000000;
  for (local_1c = 0; local_1c != 6; local_1c = local_1c + 1) {
    abStack_18[local_1c] = (byte)((param_5 % local_20) / (local_20 / 10));
    local_20 = local_20 / 10;
  }
  local_1c = 0;
  do {
    if (local_1c == 6) {
LAB__text__0049609f:
      if (local_1c == 6) {
        local_2c = 1;
      }
      iVar3 = local_2c * 10;
      FUN__text__004077c0(DAT_007a49fc);
      *(undefined4 *)(local_8 + 0xde614) = param_8;
      *(undefined1 *)(local_8 + 0xde617) = param_6;
      if (*(char *)(local_8 + 0xde617) == -1) {
        *(undefined4 *)(local_8 + 0xde60c) = 0;
      }
      else {
        *(undefined4 *)(local_8 + 0xde60c) = 1;
      }
      *(undefined2 *)(local_8 + 0xde626) = param_4;
      local_1c = 0;
      local_24 = 6 - local_2c;
      local_28 = 0;
      do {
        if (local_1c == local_2c) {
          local_8 = 0x49633e;
          FUN__text__0056ce80();
          return;
        }
        local_28 = local_28 | abStack_18[local_24];
        if ((local_24 == 5) || (local_28 != 0)) {
          local_30 = param_7;
          switch(param_7) {
          case 0:
            local_c = (short *)(&DAT_00619748 + (uint)abStack_18[local_24] * 0x12);
            break;
          case 1:
            local_c = (short *)(&DAT_00619748 + (abStack_18[local_24] + 10) * 0x12);
            break;
          case 2:
            local_c = (short *)(&DAT_00619748 + (abStack_18[local_24] + 0x14) * 0x12);
            break;
          case 3:
            local_c = (short *)(&DAT_00619748 + (abStack_18[local_24] + 0x1e) * 0x12);
            break;
          case 4:
            local_c = (short *)(&DAT_00619748 + (abStack_18[local_24] + 0x28) * 0x12);
            break;
          case 5:
            local_c = (short *)(&DAT_00619748 + (abStack_18[local_24] + 0x32) * 0x12);
            break;
          default:
            iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                        DAT_00619f64 + 0x33,0);
            if (iVar2 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
          FUN__text__00407870((int)*local_c,(int)local_c[1]);
          *(ushort *)(local_8 + 0xde608) =
               *(ushort *)(local_8 + 0xde608) | (ushort)*(byte *)(local_c + 8);
          *(short *)(local_8 + 0xde628) = local_c[2];
          *(short *)(local_8 + 0xde62a) = local_c[3];
          *(short *)(local_8 + 0xde62c) = local_c[4];
          *(short *)(local_8 + 0xde62e) = local_c[5];
          *(short *)(local_8 + 0xde5e8) = local_c[6];
          *(short *)(local_8 + 0xde5ea) = local_c[7];
          FUN__text__004079c0((int)(short)(param_2 - (short)(iVar3 / 2)) + local_1c * 10,
                              (int)param_3);
        }
        local_1c = local_1c + 1;
        local_24 = local_24 + 1;
      } while( true );
    }
    if (abStack_18[local_1c] != 0) {
      local_2c = 6 - local_1c;
      goto LAB__text__0049609f;
    }
    local_1c = local_1c + 1;
  } while( true );
}

