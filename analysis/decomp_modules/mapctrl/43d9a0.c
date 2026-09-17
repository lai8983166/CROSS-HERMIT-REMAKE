
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 __thiscall FUN__text__0043d9a0(int param_1,int param_2)

{
  short sVar1;
  short sVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  uint uVar11;
  int iVar12;
  undefined4 *puVar13;
  undefined4 local_c4 [33];
  uint local_40;
  int local_18;
  int local_14;
  
  puVar13 = local_c4;
  for (iVar10 = 0x30; iVar10 != 0; iVar10 = iVar10 + -1) {
    *puVar13 = 0xcccccccc;
    puVar13 = puVar13 + 1;
  }
  fVar7 = (float)param_2 / _DAT_00592774;
  uVar11 = (int)*(short *)(param_1 + 0x265a6) & 0x8000001f;
  if ((int)uVar11 < 0) {
    uVar11 = (uVar11 - 1 | 0xffffffe0) + 1;
  }
  iVar10 = -uVar11;
  uVar11 = (int)*(short *)(param_1 + 0x265a8) & 0x8000000f;
  if ((int)uVar11 < 0) {
    uVar11 = (uVar11 - 1 | 0xfffffff0) + 1;
  }
  iVar8 = -uVar11;
  sVar1 = *(short *)(param_1 + 0x265a6);
  sVar2 = *(short *)(param_1 + 0x265a8);
  for (local_18 = 0; local_18 != 0x25; local_18 = local_18 + 1) {
    for (local_14 = 0; local_14 != 0x21; local_14 = local_14 + 1) {
      iVar12 = local_14 + ((int)((int)sVar1 + ((int)sVar1 >> 0x1f & 0x1fU)) >> 5);
      iVar9 = local_18 + ((int)((int)sVar2 + ((int)sVar2 >> 0x1f & 0xfU)) >> 4);
      local_40 = (uint)*(byte *)(*(int *)(param_1 + 0x2659c) + 0x15 +
                                (iVar9 * *(short *)(*(int *)(param_1 + 0x2659c) + 4) + iVar12) * 6);
      local_40 = local_40 << 0x10 | 0xff000000 | local_40 << 8 | local_40;
      fVar3 = (float)(iVar12 * 0x20) / (float)(int)**(short **)(param_1 + 0x2659c);
      fVar4 = (float)(iVar9 * 0x10) / (float)(int)*(short *)(*(int *)(param_1 + 0x2659c) + 2);
      fVar5 = (float)(iVar12 * 0x20 + 0x20) / (float)(int)**(short **)(param_1 + 0x2659c);
      fVar6 = (float)(iVar9 * 0x10 + 0x10) / (float)(int)*(short *)(*(int *)(param_1 + 0x2659c) + 2)
      ;
      *(float *)(param_1 + local_18 * 0x1080 + 0x138 + local_14 * 0x80) = fVar7;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x13c + local_14 * 0x80) = 0x3f800000;
      *(float *)(param_1 + local_18 * 0x1080 + 0x148 + local_14 * 0x80) = fVar3;
      *(float *)(param_1 + local_18 * 0x1080 + 0x14c + local_14 * 0x80) = fVar4;
      *(uint *)(param_1 + local_18 * 0x1080 + 0x140 + local_14 * 0x80) = local_40;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x144 + local_14 * 0x80) = 0;
      *(float *)(param_1 + 0x130 + local_18 * 0x1080 + local_14 * 0x80) =
           (float)(iVar10 + local_14 * 0x20);
      *(float *)(param_1 + local_18 * 0x1080 + 0x134 + local_14 * 0x80) =
           (float)(iVar8 + 0x1e + local_18 * 0x10);
      *(float *)(param_1 + local_18 * 0x1080 + 0x158 + local_14 * 0x80) = fVar7;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x15c + local_14 * 0x80) = 0x3f800000;
      *(float *)(param_1 + local_18 * 0x1080 + 0x168 + local_14 * 0x80) = fVar5;
      *(float *)(param_1 + local_18 * 0x1080 + 0x16c + local_14 * 0x80) = fVar4;
      *(uint *)(param_1 + local_18 * 0x1080 + 0x160 + local_14 * 0x80) = local_40;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x164 + local_14 * 0x80) = 0;
      *(float *)(param_1 + local_18 * 0x1080 + 0x150 + local_14 * 0x80) =
           (float)(iVar10 + 0x20 + local_14 * 0x20);
      *(float *)(param_1 + local_18 * 0x1080 + 0x154 + local_14 * 0x80) =
           (float)(iVar8 + 0x1e + local_18 * 0x10);
      *(float *)(param_1 + local_18 * 0x1080 + 0x178 + local_14 * 0x80) = fVar7;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x17c + local_14 * 0x80) = 0x3f800000;
      *(float *)(param_1 + local_18 * 0x1080 + 0x188 + local_14 * 0x80) = fVar5;
      *(float *)(param_1 + local_18 * 0x1080 + 0x18c + local_14 * 0x80) = fVar6;
      *(uint *)(param_1 + local_18 * 0x1080 + 0x180 + local_14 * 0x80) = local_40;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x184 + local_14 * 0x80) = 0;
      *(float *)(param_1 + local_18 * 0x1080 + 0x170 + local_14 * 0x80) =
           (float)(iVar10 + 0x20 + local_14 * 0x20);
      *(float *)(param_1 + local_18 * 0x1080 + 0x174 + local_14 * 0x80) =
           (float)(iVar8 + 0x2e + local_18 * 0x10);
      *(float *)(param_1 + local_18 * 0x1080 + 0x198 + local_14 * 0x80) = fVar7;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x19c + local_14 * 0x80) = 0x3f800000;
      *(float *)(param_1 + local_18 * 0x1080 + 0x1a8 + local_14 * 0x80) = fVar3;
      *(float *)(param_1 + local_18 * 0x1080 + 0x1ac + local_14 * 0x80) = fVar6;
      *(uint *)(param_1 + local_18 * 0x1080 + 0x1a0 + local_14 * 0x80) = local_40;
      *(undefined4 *)(param_1 + local_18 * 0x1080 + 0x1a4 + local_14 * 0x80) = 0;
      *(float *)(param_1 + local_18 * 0x1080 + 400 + local_14 * 0x80) =
           (float)(iVar10 + local_14 * 0x20);
      *(float *)(param_1 + local_18 * 0x1080 + 0x194 + local_14 * 0x80) =
           (float)(iVar8 + 0x2e + local_18 * 0x10);
    }
  }
  return 0;
}

