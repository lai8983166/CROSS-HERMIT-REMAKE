
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN__text__005545c0(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  
  uVar5 = (uint)*param_3;
  uVar6 = (uint)((ulonglong)*param_3 >> 0x20);
  uVar7 = (uint)param_3[1];
  fVar8 = (float)((ulonglong)param_3[1] >> 0x20);
  fVar1 = (float)*param_2;
  fVar2 = (float)((ulonglong)*param_2 >> 0x20);
  fVar3 = (float)param_2[1];
  fVar4 = (float)((ulonglong)param_2[1] >> 0x20);
  fVar9 = (float)(uVar5 ^ _UNK_0080c108);
  fVar11 = (float)(uVar5 ^ _UNK_0080c10c);
  fVar13 = (float)(uVar6 ^ _UNK_0080c0f8);
  fVar14 = (float)(uVar6 ^ _UNK_0080c0fc);
  fVar10 = (float)(uVar7 ^ _UNK_0080c0e8);
  fVar12 = (float)(uVar7 ^ _UNK_0080c0ec);
  *param_1 = CONCAT44(fVar8 * fVar2 + (float)(uVar5 ^ _UNK_0080c104) * fVar3 +
                      (float)(uVar6 ^ _UNK_0080c0f4) * fVar4 +
                      (float)(uVar7 ^ _UNK_0080c0e4) * fVar1,
                      fVar8 * fVar1 + (float)(uVar5 ^ _DAT_0080c100) * fVar4 +
                      (float)(uVar6 ^ _DAT_0080c0f0) * fVar3 +
                      (float)(uVar7 ^ _DAT_0080c0e0) * fVar2);
  param_1[1] = CONCAT44(fVar8 * fVar4 + fVar11 * fVar1 + fVar14 * fVar2 + fVar12 * fVar3,
                        fVar8 * fVar3 + fVar9 * fVar2 + fVar13 * fVar1 + fVar10 * fVar4);
  return param_1;
}

