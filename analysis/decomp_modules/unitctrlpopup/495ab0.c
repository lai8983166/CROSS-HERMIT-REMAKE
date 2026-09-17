
void __thiscall FUN__text__00495ab0(int param_1,byte *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  uint local_24;
  undefined4 local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  short *local_10;
  char *local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((*param_2 & 0x80) == 0) &&
     (iVar2 = FUN__text__00424f80("(pw->mode & 0x80)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                  DAT_00619f60 + 0x36,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (char *)(*(int *)(param_2 + 0xc) + (char)param_2[10] * 8);
  local_10 = (short *)(&DAT_00619748 + local_c[4] * 0x12);
  local_24 = (uint)param_2[1];
  switch(local_24) {
  case 0:
  case 9:
    local_20 = 0xff808080;
    break;
  case 1:
  case 10:
    local_20 = 0xff803030;
    break;
  case 2:
  case 0xb:
    local_20 = 0xff808030;
    goto LAB__text__00495c70;
  case 3:
  case 0xc:
    local_20 = 0xff303080;
LAB__text__00495c70:
    local_14 = local_8 + 0x80aec + *(short *)(param_2 + 4) * 0x520;
    if ((*(byte *)(local_14 + 8) & 0x80) != 0) {
      local_18 = ((*(int *)(local_14 + 0x2ec) >> 0x10) + (int)*local_c + (int)(char)param_2[2]) -
                 (int)*(short *)(local_8 + 0x2a30e);
      local_1c = ((*(int *)(local_14 + 0x2f0) >> 0x10) + 0x1e + (int)local_c[1] +
                 (int)(char)param_2[3]) - (int)*(short *)(local_8 + 0x2a310);
      iVar2 = FUN__text__0046b130(local_18 & 0xffff,local_1c);
      if (iVar2 != 0) {
        FUN__text__00495fe0(local_18 & 0xffff,local_1c & 0xffff,0x348,(int)*(short *)(param_2 + 8),
                            (uint)(byte)local_c[3] - (uint)param_2[0xb],
                            *(undefined4 *)(&DAT_00619f08 + (uint)param_2[1] * 4),local_20);
      }
    }
    goto LAB__text__00495f7e;
  case 4:
  case 0xd:
    local_20 = 0xff308030;
    break;
  case 5:
  case 0xe:
    local_20 = 0xff803080;
    break;
  case 6:
  case 7:
  case 8:
  case 0xf:
  case 0x10:
  case 0x11:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f60 + 0x6c,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__00495f7e;
  default:
    local_14 = local_8 + 0x80aec + *(short *)(param_2 + 4) * 0x520;
    if ((*(byte *)(local_14 + 8) & 0x80) != 0) {
      local_18 = ((*(int *)(local_14 + 0x2ec) >> 0x10) + (int)*local_c + (int)(char)param_2[2]) -
                 (int)*(short *)(local_8 + 0x2a30e);
      local_1c = ((*(int *)(local_14 + 0x2f0) >> 0x10) + 0x1e + (int)local_c[1] +
                 (int)(char)param_2[3]) - (int)*(short *)(local_8 + 0x2a310);
      iVar2 = FUN__text__0046b130(local_18 & 0xffff,local_1c);
      if (iVar2 != 0) {
        FUN__text__004077c0(DAT_007a49fc);
        FUN__text__00407870((int)*local_10,(int)local_10[1]);
        *(ushort *)(local_8 + 0xde608) =
             *(ushort *)(local_8 + 0xde608) | (ushort)*(byte *)(local_10 + 8);
        *(undefined2 *)(local_8 + 0xde626) = 0x348;
        *(short *)(local_8 + 0xde628) = local_10[2];
        *(short *)(local_8 + 0xde62a) = local_10[3];
        *(short *)(local_8 + 0xde62c) = local_10[4];
        *(short *)(local_8 + 0xde62e) = local_10[5];
        *(char *)(local_8 + 0xde617) = local_c[3];
        *(undefined1 *)(local_8 + 0xde616) = 0x80;
        *(undefined1 *)(local_8 + 0xde615) = 0x80;
        *(undefined1 *)(local_8 + 0xde614) = 0x80;
        *(short *)(local_8 + 0xde5e8) = local_10[6];
        *(short *)(local_8 + 0xde5ea) = local_10[7];
        if (*(char *)(local_8 + 0xde617) == -1) {
          *(undefined4 *)(local_8 + 0xde60c) = 0;
        }
        else {
          *(undefined4 *)(local_8 + 0xde60c) = 1;
        }
        FUN__text__004079c0(local_18,local_1c);
      }
    }
    goto LAB__text__00495f7e;
  }
  local_14 = local_8 + 0x80aec + *(short *)(param_2 + 4) * 0x520;
  if ((*(byte *)(local_14 + 8) & 0x80) != 0) {
    local_18 = ((*(int *)(local_14 + 0x2ec) >> 0x10) + (int)*local_c + (int)(char)param_2[2]) -
               (int)*(short *)(local_8 + 0x2a30e);
    local_1c = ((*(int *)(local_14 + 0x2f0) >> 0x10) + 0x1e + (int)local_c[1] +
               (int)(char)param_2[3]) - (int)*(short *)(local_8 + 0x2a310);
    iVar2 = FUN__text__0046b130(local_18 & 0xffff,local_1c);
    if (iVar2 != 0) {
      FUN__text__00495fe0(local_18 & 0xffff,local_1c & 0xffff,0x348,(int)*(short *)(param_2 + 8),
                          (uint)(byte)local_c[3] - (uint)param_2[0xb],
                          *(undefined4 *)(&DAT_00619f08 + (uint)param_2[1] * 4),local_20);
    }
  }
LAB__text__00495f7e:
  local_8 = 0x495f8b;
  FUN__text__0056ce80();
  return;
}

