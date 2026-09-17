
void FUN__text__00491ef0(int param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_cc [16];
  uint local_8c;
  int local_88;
  uint local_84;
  uint local_80;
  uint local_7c;
  undefined1 local_78 [44];
  undefined1 local_4c [44];
  undefined4 local_20;
  undefined *local_1c;
  int local_18;
  undefined *local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_cc;
  for (iVar2 = 0x32; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  local_14 = &DAT_006b2d88 + iVar2;
  local_c = &DAT_006c2dc8 + *(short *)(param_3 + 4) * 0x48;
  local_10 = &DAT_006c2dc8 + *(short *)(&DAT_006b2da0 + iVar2) * 0x48;
  local_18 = FUN__text__004de8f0((int)*(short *)(param_3 + 4));
  local_1c = &DAT_00611538 + *(short *)(param_3 + 4) * 0x10;
  iVar2 = FUN__text__0046c9f0((int)*(short *)(param_3 + 4));
  if ((iVar2 == 0) && (*(short *)(local_1c + 0xc) != 0)) {
    local_80 = (uint)(byte)local_c[5];
    switch(local_80) {
    case 0:
    case 3:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619244 + 0x18,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 1:
    case 4:
      local_20 = 0;
      break;
    case 2:
      local_20 = 1;
    }
    local_84 = (uint)*(byte *)(local_18 + 6);
    switch(local_84) {
    case 0:
      break;
    case 1:
    case 4:
      if (*(char *)(param_3 + 6) != '\x04') {
        FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),local_20);
      }
      break;
    case 2:
    case 5:
      if (*(char *)(param_3 + 6) != '\x04') {
        FUN__text__00493180(param_2,*(undefined2 *)(param_3 + 10));
      }
      break;
    case 3:
    case 6:
      if (*(char *)(param_3 + 6) != '\x04') {
        FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),local_20);
      }
      if (*(char *)(param_3 + 6) != '\x04') {
        FUN__text__00493180(param_2,*(undefined2 *)(param_3 + 10));
      }
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619244 + 0x35,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  else {
    local_c = &DAT_006c2dc8 + *(short *)(local_14 + 0x18) * 0x48;
    local_7c = (uint)(0 < *(short *)(param_3 + 10));
    local_8c = (uint)(byte)(&DAT_006c2dcd)[*(short *)(local_14 + 0x18) * 0x48];
    switch(local_8c) {
    case 0:
    case 1:
    case 4:
      if ((local_7c != 0) || (*(char *)(param_3 + 6) != '\x04')) {
        FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),0);
      }
      break;
    case 2:
      if ((local_7c != 0) || (*(char *)(param_3 + 6) != '\x04')) {
        FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),1);
      }
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619244 + 0x5e,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    iVar2 = FUN__text__0046c9f0((int)*(short *)(param_3 + 4));
    if (iVar2 != 0) goto LAB__text__004922bd;
    local_c = &DAT_006c2dc8 + *(short *)(param_3 + 4) * 0x48;
  }
  if ((local_c[0x1a] != '\0') && (*(char *)(param_3 + 6) != '\x04')) {
    FUN__text__004deaa0(param_1,local_4c);
    FUN__text__0046b3e0(param_1,local_4c);
    FUN__text__004deaa0(param_2,local_78);
    FUN__text__0046b3e0(param_2,local_78);
    FUN__text__0048b2e0(local_c[0x1a],(int)*(short *)(param_3 + 4),param_1,param_2,local_4c,local_78
                       );
  }
  local_88 = (int)*(short *)(param_3 + 4);
  if (local_88 != 0xc) {
    if (local_88 == 0x1d) {
      FUN__text__00492320(param_1,param_2,param_3);
      goto LAB__text__004922bd;
    }
    if (local_88 != 0x2f) goto LAB__text__004922bd;
  }
  FUN__text__004924e0(param_1,param_2,param_3);
LAB__text__004922bd:
  local_8 = 0x4922d4;
  FUN__text__0056ce80();
  return;
}

