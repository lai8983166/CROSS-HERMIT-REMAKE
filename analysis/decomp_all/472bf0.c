
void FUN__text__00472bf0(short param_1,short param_2,undefined2 param_3,int param_4,int param_5,
                        int param_6,uint param_7)

{
  int iVar1;
  undefined4 *puVar2;
  bool bVar3;
  undefined4 local_70 [16];
  int local_30;
  undefined4 local_2c;
  uint local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  byte abStack_14 [12];
  int local_8;
  
  puVar2 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (999999 < param_4) {
    param_4 = 999999;
  }
  if (param_4 < 0) {
    param_4 = 0;
  }
  bVar3 = param_5 < 0;
  if (bVar3) {
    param_5 = -param_5;
  }
  local_20 = (uint)bVar3;
  local_1c = 1000000;
  for (local_18 = 0; local_18 != 6; local_18 = local_18 + 1) {
    abStack_14[local_18] = (byte)((param_4 % local_1c) / (local_1c / 10));
    local_1c = local_1c / 10;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(char *)(local_8 + 0xde797) = (char)(param_7 >> 0x18);
  if (*(char *)(local_8 + 0xde797) == -1) {
    *(undefined4 *)(local_8 + 0xde78c) = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0xde78c) = 1;
  }
  *(char *)(local_8 + 0xde796) = (char)((param_7 & 0xff0000) / 0x20000);
  *(char *)(local_8 + 0xde795) = (char)((param_7 & 0xff00) / 0x200);
  *(char *)(local_8 + 0xde794) = (char)((param_7 & 0xff) / 2);
  *(undefined2 *)(local_8 + 0xde7a6) = param_3;
  FUN__text__00407870(0x5a,0x14);
  local_24 = 6 - param_5;
  local_28 = 0;
  for (local_18 = 0; local_18 != param_5; local_18 = local_18 + 1) {
    local_28 = local_28 | abStack_14[local_24];
    local_30 = param_6;
    local_2c = 7;
    *(ushort *)(local_8 + 0xde788) = *(ushort *)(local_8 + 0xde788) | 0x40;
    *(undefined2 *)(local_8 + 0xde768) =
         *(undefined2 *)(&DAT_00618818 + (uint)abStack_14[local_24] * 0x10 + param_6 * 0xa0);
    *(undefined2 *)(local_8 + 0xde76a) =
         *(undefined2 *)(&DAT_0061881c + (uint)abStack_14[local_24] * 0x10 + param_6 * 0xa0);
    *(undefined2 *)(local_8 + 0xde7a8) =
         *(undefined2 *)(&DAT_00618810 + (uint)abStack_14[local_24] * 0x10 + param_6 * 0xa0);
    *(undefined2 *)(local_8 + 0xde7aa) =
         *(undefined2 *)(&DAT_00618814 + (uint)abStack_14[local_24] * 0x10 + param_6 * 0xa0);
    *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
    *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
    if (local_20 == 0) {
      if ((local_24 == 5) || (local_28 != 0)) {
        FUN__text__004079c0((int)param_1 + local_18 * 7,(int)param_2);
      }
    }
    else {
      FUN__text__004079c0((int)param_1 + local_18 * 7,(int)param_2);
    }
    local_24 = local_24 + 1;
  }
  local_8 = 0x472f2d;
  FUN__text__0056ce80();
  return;
}

