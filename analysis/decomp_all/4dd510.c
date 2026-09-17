
void FUN__text__004dd510(int param_1,undefined4 param_2,ushort *param_3,int param_4)

{
  uint3 *puVar1;
  short sVar2;
  ushort uVar3;
  code *pcVar4;
  uint3 uVar5;
  uint3 uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  ushort uVar11;
  uint uVar12;
  int iVar13;
  short *psVar14;
  undefined4 *puVar15;
  undefined4 local_70 [16];
  undefined *local_30;
  short local_2c;
  short sStack_2a;
  ushort local_28;
  short sStack_26;
  short local_24;
  short sStack_22;
  ushort local_20;
  byte bStack_1e;
  ushort local_1c;
  byte bStack_1a;
  byte bStack_19;
  byte local_18;
  byte bStack_17;
  char cStack_16;
  byte bStack_15;
  undefined1 local_14;
  undefined1 uStack_13;
  undefined1 uStack_12;
  undefined1 uStack_11;
  byte local_10;
  short sStack_e;
  ushort local_c;
  byte bStack_a;
  undefined2 local_8;
  undefined2 uStack_6;
  
  puVar15 = local_70;
  for (iVar13 = 0x1b; iVar13 != 0; iVar13 = iVar13 + -1) {
    *puVar15 = 0xcccccccc;
    puVar15 = puVar15 + 1;
  }
  if (((param_1 < 0) || (0x1ff < param_1)) &&
     (iVar13 = FUN__text__00424f80(&DAT_005ca44c,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                   DAT_00738c90 + 4,0), iVar13 != 0)) {
    pcVar4 = (code *)swi(3);
    (*pcVar4)();
    return;
  }
  if ((param_1 != 0) && (param_1 != 0xffff)) {
    _memset(&local_2c,0,0x28);
    param_1 = param_1 * 0x38;
    local_30 = &DAT_006d5118 + param_1;
    local_2c = (short)*(uint *)(&DAT_006d513a + param_1);
    sStack_2a = (short)*(uint *)(&DAT_006d513c + param_1);
    local_28 = *(ushort *)(&DAT_006d513e + param_1);
    uVar7 = *(uint *)(&DAT_006d513c + param_1);
    sStack_26 = (short)*(uint *)(&DAT_006d5124 + param_1);
    local_24 = (short)*(uint *)(&DAT_006d5126 + param_1);
    uVar8 = *(uint *)(&DAT_006d5124 + param_1);
    sStack_22 = (short)*(uint *)(&DAT_006d5128 + param_1);
    uVar9 = *(uint *)(&DAT_006d5126 + param_1);
    local_20 = *(ushort *)(&DAT_006d512a + param_1);
    uVar10 = *(uint *)(&DAT_006d5128 + param_1);
    bStack_1e = (&DAT_006d5130)[param_1];
    local_1c = *(ushort *)(&DAT_006d5132 + param_1);
    bStack_1a = (&DAT_006d5139)[param_1];
    bStack_19 = (&DAT_006d5134)[param_1];
    local_18 = (&DAT_006d5136)[param_1];
    bStack_17 = (&DAT_006d5135)[param_1];
    cStack_16 = (char)*(ushort *)(&DAT_006d5137 + param_1);
    bStack_15 = (&DAT_006d5138)[param_1];
    uVar11 = *(ushort *)(&DAT_006d5137 + param_1);
    puVar1 = (uint3 *)(&DAT_006d512c + param_1);
    sVar2 = (short)*puVar1;
    local_14 = (undefined1)sVar2;
    uStack_13 = (undefined1)((ushort)sVar2 >> 8);
    uVar3 = *(ushort *)(&DAT_006d512e + param_1);
    uVar6 = *puVar1;
    uVar5 = *puVar1;
    uStack_12 = (undefined1)uVar3;
    uStack_11 = (undefined1)(uVar3 >> 8);
    local_10 = (&DAT_006d514c)[param_1];
    sStack_e = (short)*(uint *)(&DAT_006d5148 + param_1);
    local_c = *(ushort *)(&DAT_006d514a + param_1);
    uVar12 = *(uint *)(&DAT_006d5148 + param_1);
    bStack_a = (&DAT_006d5140)[param_1];
    iVar13 = *(int *)(&DAT_006d5144 + param_1);
    local_8 = (undefined2)iVar13;
    uStack_6 = (undefined2)((uint)iVar13 >> 0x10);
    if (param_4 == 0) {
      if ((uint)*param_3 + (*(uint *)(&DAT_006d513a + param_1) & 0xffff) < 999) {
        *param_3 = *param_3 + local_2c;
      }
      else {
        *param_3 = 999;
      }
      if ((uint)param_3[1] + (uVar7 & 0xffff) < 999) {
        param_3[1] = param_3[1] + sStack_2a;
      }
      else {
        param_3[1] = 999;
      }
      if ((uint)param_3[2] + (uint)local_28 < 999) {
        param_3[2] = param_3[2] + local_28;
      }
      else {
        param_3[2] = 999;
      }
      if ((uint)param_3[3] + (uVar8 & 0xffff) < 999) {
        param_3[3] = param_3[3] + sStack_26;
      }
      else {
        param_3[3] = 999;
      }
      if ((uint)param_3[4] + (uVar9 & 0xffff) < 999) {
        param_3[4] = param_3[4] + local_24;
      }
      else {
        param_3[4] = 999;
      }
      if ((uint)param_3[5] + (uVar10 & 0xffff) < 999) {
        param_3[5] = param_3[5] + sStack_22;
      }
      else {
        param_3[5] = 999;
      }
      if ((uint3)((uint3)param_3[6] + (uint3)local_20) < 999) {
        param_3[6] = param_3[6] + local_20;
      }
      else {
        param_3[6] = 999;
      }
      if ((uint)(byte)param_3[7] + (uint)bStack_1e < 0x20) {
        *(byte *)(param_3 + 7) = (char)param_3[7] + bStack_1e;
      }
      else {
        *(undefined1 *)(param_3 + 7) = 0x20;
      }
      if ((uint3)((uint3)param_3[8] + (uint3)local_1c) < 999) {
        param_3[8] = param_3[8] + local_1c;
      }
      else {
        param_3[8] = 999;
      }
      if ((ushort)((ushort)(byte)param_3[9] + (ushort)bStack_1a) < 0x7f) {
        *(byte *)(param_3 + 9) = (char)param_3[9] + bStack_1a;
      }
      else {
        *(undefined1 *)(param_3 + 9) = 0x7f;
      }
      if ((ushort)((ushort)*(byte *)((int)param_3 + 0x13) + (ushort)bStack_19) < 0xff) {
        *(byte *)((int)param_3 + 0x13) = *(char *)((int)param_3 + 0x13) + bStack_19;
      }
      else {
        *(undefined1 *)((int)param_3 + 0x13) = 0xff;
      }
      if ((ushort)((ushort)(byte)param_3[10] + (ushort)local_18) < 100) {
        *(byte *)(param_3 + 10) = (char)param_3[10] + local_18;
      }
      else {
        *(undefined1 *)(param_3 + 10) = 100;
      }
      if ((ushort)((ushort)*(byte *)((int)param_3 + 0x15) + (ushort)bStack_17) < 0xff) {
        *(byte *)((int)param_3 + 0x15) = *(char *)((int)param_3 + 0x15) + bStack_17;
      }
      else {
        *(undefined1 *)((int)param_3 + 0x15) = 0xff;
      }
      if ((ushort)((ushort)(byte)param_3[0xb] + (uVar11 & 0xff)) < 0xff) {
        *(char *)(param_3 + 0xb) = (char)param_3[0xb] + cStack_16;
      }
      else {
        *(undefined1 *)(param_3 + 0xb) = 0xff;
      }
      if ((ushort)((ushort)*(byte *)((int)param_3 + 0x17) + (ushort)bStack_15) < 100) {
        *(byte *)((int)param_3 + 0x17) = *(char *)((int)param_3 + 0x17) + bStack_15;
      }
      else {
        *(undefined1 *)((int)param_3 + 0x17) = 100;
      }
      if ((uint)(byte)param_3[0xe] + (uint)local_10 < 100) {
        *(byte *)(param_3 + 0xe) = (char)param_3[0xe] + local_10;
      }
      else {
        *(undefined1 *)(param_3 + 0xe) = 100;
      }
      if ((uint)param_3[0xf] + (uVar12 & 0xffff) < 999) {
        param_3[0xf] = param_3[0xf] + sStack_e;
      }
      else {
        param_3[0xf] = 999;
      }
      if ((uint3)((uint3)param_3[0x10] + (uint3)local_c) < 999) {
        param_3[0x10] = param_3[0x10] + local_c;
      }
      else {
        param_3[0x10] = 999;
      }
      if ((uint)(byte)param_3[0x11] + (uint)bStack_a < 0x7f) {
        *(byte *)(param_3 + 0x11) = (char)param_3[0x11] + bStack_a;
      }
      else {
        *(undefined1 *)(param_3 + 0x11) = 0x7f;
      }
      if ((param_3[0xc] == 0xffff) || ((uVar5 & 0xffff) == 0xffff)) {
        param_3[0xc] = 0xffff;
      }
      else if ((uint3)((uint3)param_3[0xc] + (uVar6 & 0xffff)) < 0xffff) {
        param_3[0xc] = param_3[0xc] + sVar2;
      }
      else {
        param_3[0xc] = 0xffff;
      }
      if ((param_3[0xd] == 0xffff) || (uVar3 == 0xffff)) {
        param_3[0xd] = 0xffff;
      }
      else if ((uint3)((uint3)param_3[0xd] + (uint3)uVar3) < 0xffff) {
        param_3[0xd] = param_3[0xd] + uVar3;
      }
      else {
        param_3[0xd] = 0xffff;
      }
      if ((*(int *)(param_3 + 0x12) == 0xffff) || (iVar13 == 0xffff)) {
        param_3[0x12] = 0xffff;
        param_3[0x13] = 0;
      }
      else if (*(int *)(param_3 + 0x12) + iVar13 < 0xffff) {
        *(int *)(param_3 + 0x12) = *(int *)(param_3 + 0x12) + iVar13;
      }
      else {
        param_3[0x12] = 0xffff;
        param_3[0x13] = 0;
      }
    }
    else {
      _memset(param_3,0,0x28);
      psVar14 = &local_2c;
      for (iVar13 = 10; iVar13 != 0; iVar13 = iVar13 + -1) {
        *(undefined4 *)param_3 = *(undefined4 *)psVar14;
        psVar14 = psVar14 + 2;
        param_3 = param_3 + 2;
      }
    }
  }
  local_8 = 0xdba0;
  uStack_6 = 0x4d;
  FUN__text__0056ce80();
  return;
}

