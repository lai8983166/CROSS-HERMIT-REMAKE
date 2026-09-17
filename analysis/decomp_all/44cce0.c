
void FUN__text__0044cce0(short param_1,short param_2,undefined2 param_3,int param_4,int param_5,
                        int param_6,uint param_7)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  bool bVar4;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  uint local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  byte abStack_14 [12];
  int local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (999999 < param_4) {
    param_4 = 999999;
  }
  if (param_4 < 0) {
    param_4 = 0;
  }
  bVar4 = param_5 < 0;
  if (bVar4) {
    param_5 = -param_5;
  }
  local_20 = (uint)bVar4;
  local_1c = 1000000;
  for (local_18 = 0; local_18 != 6; local_18 = local_18 + 1) {
    abStack_14[local_18] = (byte)((param_4 % local_1c) / (local_1c / 10));
    local_1c = local_1c / 10;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(char *)(local_8 + 0x11f) = (char)(param_7 >> 0x18);
  if (*(char *)(local_8 + 0x11f) == -1) {
    *(undefined4 *)(local_8 + 0x114) = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0x114) = 1;
  }
  *(char *)(local_8 + 0x11e) = (char)((param_7 & 0xff0000) / 0x20000);
  *(char *)(local_8 + 0x11d) = (char)((param_7 & 0xff00) / 0x200);
  *(char *)(local_8 + 0x11c) = (char)((param_7 & 0xff) / 2);
  *(undefined2 *)(local_8 + 0x12e) = param_3;
  FUN__text__00407870(0x5a,5);
  local_18 = 0;
  local_24 = 6 - param_5;
  local_28 = 0;
  do {
    if (local_18 == param_5) {
      local_8 = 0x44d02c;
      FUN__text__0056ce80();
      return;
    }
    local_28 = local_28 | abStack_14[local_24];
    local_30 = param_6;
    if (param_6 == 0) {
      local_2c = 8;
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_0060679c + 0x3b,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    *(ushort *)(local_8 + 0x110) = *(ushort *)(local_8 + 0x110) | 0x40;
    *(undefined2 *)(local_8 + 0xf0) =
         *(undefined2 *)(&DAT_006066ac + (uint)abStack_14[local_24] * 8 + param_6 * 0x50);
    *(undefined2 *)(local_8 + 0xf2) =
         *(undefined2 *)(&DAT_006066ae + (uint)abStack_14[local_24] * 8 + param_6 * 0x50);
    *(undefined2 *)(local_8 + 0x130) =
         *(undefined2 *)(&DAT_006066a8 + (uint)abStack_14[local_24] * 8 + param_6 * 0x50);
    *(undefined2 *)(local_8 + 0x132) =
         *(undefined2 *)(&DAT_006066aa + (uint)abStack_14[local_24] * 8 + param_6 * 0x50);
    *(short *)(local_8 + 0x134) = *(short *)(local_8 + 0x130) + *(short *)(local_8 + 0xf0);
    *(short *)(local_8 + 0x136) = *(short *)(local_8 + 0x132) + *(short *)(local_8 + 0xf2);
    if (local_20 == 0) {
      if ((local_24 == 5) || (local_28 != 0)) {
        FUN__text__004079c0((int)param_1 + local_2c * local_18,(int)param_2);
      }
    }
    else {
      FUN__text__004079c0((int)param_1 + local_2c * local_18,(int)param_2);
    }
    local_18 = local_18 + 1;
    local_24 = local_24 + 1;
  } while( true );
}

