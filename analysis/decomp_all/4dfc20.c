
/* WARNING: Removing unreachable block (ram,0x004e08ed) */
/* WARNING: Removing unreachable block (ram,0x004e0916) */

void FUN__text__004dfc20(undefined2 *param_1,undefined2 *param_2)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  code *pcVar8;
  int iVar9;
  undefined4 *puVar10;
  undefined4 local_8c [16];
  int local_4c;
  char local_48;
  int local_44;
  char local_40;
  int local_3c;
  int local_38;
  char local_34;
  int local_30;
  uint local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  undefined *local_c;
  undefined *local_8;
  
  puVar10 = local_8c;
  for (iVar9 = 0x22; iVar9 != 0; iVar9 = iVar9 + -1) {
    *puVar10 = 0xcccccccc;
    puVar10 = puVar10 + 1;
  }
  local_8 = &DAT_006b2d88 + (short)param_1[1] * 0x40;
  local_c = &DAT_006c2dc8 + *(short *)(&DAT_006b2da0 + (short)param_1[1] * 0x40) * 0x48;
  _memset(param_2,0,0xb0);
  bVar1 = *(byte *)((int)param_1 + 5);
  local_14 = (uint)bVar1;
  bVar2 = *(byte *)(param_1 + 3);
  local_18 = (uint)bVar2;
  bVar3 = *(byte *)((int)param_1 + 7);
  local_1c = (uint)bVar3;
  bVar4 = *(byte *)(param_1 + 4);
  local_20 = (uint)bVar4;
  bVar5 = *(byte *)((int)param_1 + 9);
  local_24 = (uint)bVar5;
  bVar6 = *(byte *)(param_1 + 5);
  local_28 = (uint)bVar6;
  bVar7 = *(byte *)((int)param_1 + 0xb);
  local_2c = (uint)bVar7;
  *param_2 = *param_1;
  param_2[1] = *param_1;
  *(byte *)(param_2 + 2) = bVar1;
  *(byte *)((int)param_2 + 5) = bVar2;
  *(byte *)(param_2 + 3) = bVar3;
  *(byte *)((int)param_2 + 7) = bVar4;
  *(byte *)(param_2 + 4) = bVar5;
  *(byte *)((int)param_2 + 9) = bVar6;
  *(byte *)(param_2 + 5) = bVar7;
  param_2[6] = param_1[1];
  *(undefined1 *)(param_2 + 7) = *(undefined1 *)(param_1 + 6);
  *(undefined1 *)((int)param_2 + 0xf) = 1;
  param_2[8] = 0;
  param_2[9] = 0;
  param_2[10] = (short)((local_28 * 300) / 100) + (short)((local_14 * 100) / 100) +
                (short)((local_18 * 100) / 100);
  param_2[10] = param_2[10];
  param_2[10] = param_2[10];
  param_2[10] = (short)((int)((int)(short)param_2[10] * (uint)*(ushort *)(local_8 + 6)) / 100);
  param_2[0xb] = param_2[10];
  param_2[0xc] = (*(short *)(local_8 + 8) - (short)((local_28 * 100) / 100)) -
                 (short)((local_14 * 0x32) / 100);
  param_2[0xd] = (short)((local_2c * 300) / 100) + (short)((local_24 * 100) / 100) +
                 (short)((local_20 * 100) / 100);
  param_2[0xe] = param_2[0xd];
  param_2[0xf] = (*(short *)(local_8 + 0xc) - (short)((local_2c * 100) / 100)) -
                 (short)((local_20 * 0x32) / 100);
  param_2[0xf] = param_2[0xf];
  *(int *)(param_2 + 0x10) = *(int *)(&DAT_006e4528 + (uint)*(byte *)(param_2 + 7) * 4) * 0x3c;
  *(undefined4 *)(param_2 + 0x12) = *(undefined4 *)(param_2 + 0x10);
  *(uint *)(param_2 + 0x14) = (((uint)*(byte *)(param_1 + 6) * 10) / 100 + 10) * 0xe10;
  *(char *)(param_2 + 0x16) = local_8[0x12] + (char)((local_1c * 10) / 100);
  param_2[0x17] =
       *(short *)(local_8 + 0x14) +
       (short)((((int)(uint)*(ushort *)(local_8 + 0x14) >> 1) * local_18) / 100);
  *(undefined *)(param_2 + 0x18) = (&DAT_00738c10)[(byte)local_8[0x16]];
  param_2[0x19] = *(undefined2 *)(local_c + 10);
  param_2[0x1a] = *(undefined2 *)(local_c + 0xe);
  *(undefined *)(param_2 + 0x1b) = local_c[0x10];
  local_30 = (byte)local_8[2] - 1;
  switch(local_30) {
  case 0:
  case 5:
    local_10 = (uint)(byte)local_c[0x12];
    break;
  case 1:
  case 6:
    local_10 = (uint)(byte)local_c[0x12];
    break;
  case 2:
  case 7:
    local_34 = *(char *)(param_1 + 0x17);
    if ((((local_34 != '\x01') && (local_34 != '\x02')) && (local_34 != '\x03')) &&
       (iVar9 = FUN__text__00424f80(&DAT_005ca5b0,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb0 + 0x96,0), iVar9 != 0)) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  case 3:
  case 8:
    local_10 = (uint)(byte)local_c[0x12] + (int)(local_20 * 10) / 100;
    break;
  case 4:
  case 9:
    local_10 = (uint)(byte)local_c[0x12] + (local_24 * 10) / 100;
    break;
  default:
    iVar9 = FUN__text__00424f80(&DAT_005ca584,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb0 + 0xa3,0);
    if (iVar9 != 0) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  }
  *(undefined1 *)((int)param_2 + 0x37) = (undefined1)local_10;
  if (local_c[0x18] == '\x06') {
    *(undefined *)((int)param_2 + 0x37) = local_c[0x16];
  }
  local_38 = (byte)local_8[2] - 1;
  switch(local_38) {
  case 0:
  case 5:
    local_10 = (uint)(byte)local_c[0x14] + (int)(local_14 * 0x32) / 100;
    break;
  case 1:
  case 6:
    local_10 = (uint)(byte)local_c[0x14] + (int)(local_18 * 100) / 100;
    break;
  case 2:
  case 7:
    local_10 = (uint)(byte)local_c[0x14] + (int)(local_1c * 0x4b) / 100;
    break;
  case 3:
  case 8:
    local_10 = 100;
    break;
  case 4:
  case 9:
    local_10 = 100;
    break;
  default:
    iVar9 = FUN__text__00424f80(&DAT_005ca584,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb0 + 200,0);
    if (iVar9 != 0) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  }
  param_2[0x1c] = (undefined2)local_10;
  local_3c = (byte)local_8[2] - 1;
  switch(local_3c) {
  case 0:
  case 5:
    local_10 = (int)((int)*(short *)(local_c + 0x20) * local_14) / 100;
    break;
  case 1:
  case 6:
    local_10 = (int)((int)*(short *)(local_c + 0x20) * local_18) / 100;
    break;
  case 2:
  case 7:
    local_40 = *(char *)(param_1 + 0x17);
    if (local_40 == '\x01') {
LAB__text__004e0229:
      local_10 = (int)((int)*(short *)(local_c + 0x20) * (local_1c + (int)local_14 / 10)) / 100;
    }
    else if (local_40 == '\x02') {
      local_10 = (int)((int)*(short *)(local_c + 0x20) * local_1c) / 100;
    }
    else {
      if (local_40 == '\x03') goto LAB__text__004e0229;
      iVar9 = FUN__text__00424f80(&DAT_005ca5b0,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                  DAT_00738cb0 + 0xe7,0);
      if (iVar9 != 0) {
        pcVar8 = (code *)swi(3);
        (*pcVar8)();
        return;
      }
    }
    break;
  case 3:
  case 8:
    local_10 = (int)((int)*(short *)(local_c + 0x20) * local_20) / 100;
    break;
  case 4:
  case 9:
    local_10 = (int)((int)*(short *)(local_c + 0x20) * local_24) / 100;
    break;
  default:
    iVar9 = FUN__text__00424f80(&DAT_005ca584,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb0 + 0xf4,0);
    if (iVar9 != 0) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  }
  param_2[0x1d] = (undefined2)local_10;
  local_44 = (byte)local_8[2] - 1;
  switch(local_44) {
  case 0:
  case 5:
    local_10 = (int)((int)*(short *)(local_c + 0x24) * local_14) / 100;
    break;
  case 1:
  case 6:
    local_10 = (int)((int)*(short *)(local_c + 0x24) * local_18) / 100;
    break;
  case 2:
  case 7:
    local_48 = *(char *)(param_1 + 0x17);
    if (local_48 != '\x01') {
      if (local_48 == '\x02') {
        local_10 = (int)((int)*(short *)(local_c + 0x24) * local_1c) / 100;
        break;
      }
      if (local_48 != '\x03') {
        iVar9 = FUN__text__00424f80(&DAT_005ca5b0,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb0 + 0x110,0);
        if (iVar9 != 0) {
          pcVar8 = (code *)swi(3);
          (*pcVar8)();
          return;
        }
        break;
      }
    }
    local_10 = (int)((int)*(short *)(local_c + 0x24) * (local_1c + (int)local_14 / 10)) / 100;
    break;
  case 3:
  case 8:
    local_10 = (int)((int)*(short *)(local_c + 0x24) * local_20) / 100;
    break;
  case 4:
  case 9:
    local_10 = (int)((int)*(short *)(local_c + 0x24) * local_24) / 100;
    break;
  default:
    iVar9 = FUN__text__00424f80(&DAT_005ca584,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb0 + 0x11d,0);
    if (iVar9 != 0) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  }
  param_2[0x1e] = (undefined2)local_10;
  param_2[0x1f] = *(undefined2 *)(local_c + 2);
  *(undefined *)(param_2 + 0x20) = local_c[5];
  *(undefined1 *)((int)param_2 + 0x41) = 100;
  param_2[0x21] = *(short *)(local_c + 0x28) + (short)((*(short *)(local_c + 0x2a) * 0x32) / 100);
  *(undefined *)(param_2 + 0x22) = local_c[0x16];
  *(undefined *)((int)param_2 + 0x45) = local_c[0x1a];
  local_4c = (byte)local_8[2] - 1;
  switch(local_4c) {
  case 0:
  case 5:
    *(uint *)(param_2 + 0x24) =
         (uint)*(ushort *)(local_c + 0x1c) + ((uint)*(ushort *)(local_c + 0x1e) * 0x32) / 100;
    break;
  case 1:
  case 6:
    *(uint *)(param_2 + 0x24) =
         (uint)*(ushort *)(local_c + 0x1c) + ((uint)*(ushort *)(local_c + 0x1e) * 0x32) / 100;
    break;
  case 2:
  case 7:
    *(uint *)(param_2 + 0x24) =
         (uint)*(ushort *)(local_c + 0x1c) + ((uint)*(ushort *)(local_c + 0x1e) * 0x32) / 100;
    break;
  case 3:
  case 8:
    *(uint *)(param_2 + 0x24) =
         (uint)*(ushort *)(local_c + 0x1c) + ((uint)*(ushort *)(local_c + 0x1e) * 0x32) / 100;
    break;
  case 4:
  case 9:
    *(uint *)(param_2 + 0x24) =
         (uint)*(ushort *)(local_c + 0x1c) + ((uint)*(ushort *)(local_c + 0x1e) * 0x32) / 100;
    break;
  default:
    iVar9 = FUN__text__00424f80(&DAT_005ca584,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb0 + 0x155,0);
    if (iVar9 != 0) {
      pcVar8 = (code *)swi(3);
      (*pcVar8)();
      return;
    }
  }
  *(char *)(param_2 + 0x26) =
       (char)((int)((byte)local_8[0x1a] * local_18) / 100) + (char)((int)(local_18 * 0x19) / 100);
  *(char *)((int)param_2 + 0x4d) =
       (char)((int)((byte)local_8[0x1b] * local_14) / 100) + (char)((int)(local_14 * 0xf) / 100);
  *(char *)(param_2 + 0x27) =
       local_8[0x1c] + (char)((int)(local_28 * 10) / 100) + (char)((int)(local_1c * 5) / 100);
  *(char *)((int)param_2 + 0x4f) = local_8[0x1d] + (char)((int)(local_24 * 0xf) / 100);
  *(char *)(param_2 + 0x28) =
       local_8[0x1e] + (char)((int)(local_2c * 5) / 100) + (char)((int)(local_20 * 10) / 100);
  param_2[0x29] = (short)((int)((int)(short)param_2[10] * (uint)(byte)local_8[0x21]) / 100);
  param_2[0x2a] = 0;
  *(undefined1 *)(param_2 + 0x2b) = 0;
  param_2[0x2c] = 0;
  param_2[0x2d] = 0;
  *(undefined4 *)(param_2 + 0x2e) = 0;
  *(undefined1 *)(param_2 + 0x30) = 0;
  *(undefined1 *)((int)param_2 + 0x61) = 0;
  *(undefined1 *)(param_2 + 0x31) = 0;
  *(undefined1 *)((int)param_2 + 99) = 0;
  *(undefined1 *)(param_2 + 0x32) = 0;
  *(undefined1 *)((int)param_2 + 0x65) = 0;
  param_2[0x33] = 0;
  param_2[0x34] = 0;
  *(undefined4 *)(param_2 + 0x36) = 0;
  *(undefined1 *)(param_2 + 0x38) = 0;
  param_2[0x39] = 0;
  param_2[0x3a] = 0;
  *(undefined4 *)(param_2 + 0x3c) = 0;
  *(undefined1 *)(param_2 + 0x3e) = 0;
  *(undefined1 *)((int)param_2 + 0x7d) = 0;
  *(undefined1 *)(param_2 + 0x3f) = 0;
  *(undefined1 *)((int)param_2 + 0x7f) = 0;
  *(undefined4 *)(param_2 + 0x40) = 0;
  param_2[0x42] = param_1[7];
  param_2[0x43] = param_1[8];
  param_2[0x44] = param_1[9];
  param_2[0x45] = param_1[10];
  param_2[0x46] = param_1[0xb];
  param_2[0x47] = param_1[0xc];
  param_2[0x48] = param_1[0xd];
  param_2[0x49] = param_1[0xe];
  *(undefined1 *)(param_2 + 0x4a) = 0;
  *(undefined1 *)((int)param_2 + 0x95) = 0;
  *(undefined1 *)(param_2 + 0x4b) = 0;
  *(undefined1 *)((int)param_2 + 0x97) = 0;
  *(undefined1 *)(param_2 + 0x4c) = 0;
  *(undefined1 *)((int)param_2 + 0x99) = 0;
  *(undefined1 *)(param_2 + 0x4d) = 0;
  *(undefined1 *)((int)param_2 + 0x9b) = 0;
  *(undefined1 *)(param_2 + 0x4e) = 0;
  *(undefined1 *)((int)param_2 + 0x9d) = 0;
  *(undefined1 *)(param_2 + 0x4f) = 0;
  *(undefined1 *)((int)param_2 + 0x9f) = 0;
  *(undefined1 *)(param_2 + 0x50) = 0;
  *(undefined1 *)((int)param_2 + 0xa1) = 0;
  *(undefined1 *)(param_2 + 0x51) = 0;
  *(undefined1 *)((int)param_2 + 0xa3) = 0;
  *(undefined1 *)(param_2 + 0x52) = 5;
  FUN__text__004e0a00(param_2);
  if (0x20 < *(byte *)((int)param_2 + 0x37)) {
    *(undefined1 *)((int)param_2 + 0x37) = 0x20;
  }
  if (0x20 < *(byte *)(param_2 + 0x22)) {
    *(undefined1 *)(param_2 + 0x22) = 0x20;
  }
  local_8 = (undefined *)0x4e092d;
  FUN__text__0056ce80();
  return;
}

