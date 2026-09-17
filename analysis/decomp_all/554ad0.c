
undefined8 * FUN__text__00554ad0(undefined8 *param_1,undefined8 *param_2,float *param_3)

{
  undefined8 uVar1;
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  if (((uint)param_3 & 0xf) == 0) {
    fVar6 = *(float *)(param_2 + 1);
    auVar3._0_4_ = fVar6 * param_3[8] + param_3[0xc];
    auVar3._4_4_ = fVar6 * param_3[9] + param_3[0xd];
    auVar3._8_4_ = fVar6 * param_3[10] + param_3[0xe];
    auVar3._12_4_ = fVar6 * param_3[0xb] + param_3[0xf];
    fVar6 = (float)*param_2;
    fVar10 = (float)((ulonglong)*param_2 >> 0x20);
    auVar2._0_4_ = fVar6 * *param_3 + fVar10 * param_3[4] + auVar3._0_4_;
    auVar2._4_4_ = fVar6 * param_3[1] + fVar10 * param_3[5] + auVar3._4_4_;
    auVar2._8_4_ = fVar6 * param_3[2] + fVar10 * param_3[6] + auVar3._8_4_;
    auVar2._12_4_ = fVar6 * param_3[3] + fVar10 * param_3[7] + auVar3._12_4_;
    auVar4 = rcpps(auVar3,auVar2);
    fVar6 = auVar4._12_4_;
    fVar6 = (fVar6 + fVar6) - fVar6 * auVar2._12_4_ * fVar6;
    *param_1 = CONCAT44(auVar2._4_4_ * fVar6,auVar2._0_4_ * fVar6);
    *(float *)(param_1 + 1) = auVar2._8_4_ * fVar6;
    return param_1;
  }
  fVar6 = *(float *)(param_2 + 1);
  fVar10 = (float)*param_2;
  fVar5 = (float)((ulonglong)*param_2 >> 0x20);
  uVar1 = *(undefined8 *)*(undefined1 (*) [16])(param_3 + 0xc);
  fVar7 = (float)*(undefined8 *)param_3 * fVar10 + (float)*(undefined8 *)(param_3 + 4) * fVar5 +
          (float)*(undefined8 *)(param_3 + 8) * fVar6 + (float)uVar1;
  fVar8 = (float)((ulonglong)*(undefined8 *)param_3 >> 0x20) * fVar10 +
          (float)((ulonglong)*(undefined8 *)(param_3 + 4) >> 0x20) * fVar5 +
          param_3[9] * fVar6 + (float)((ulonglong)uVar1 >> 0x20);
  fVar9 = (float)*(undefined8 *)(param_3 + 2) * fVar10 + (float)*(undefined8 *)(param_3 + 6) * fVar5
          + param_3[10] * fVar6 + (float)*(undefined8 *)(param_3 + 0xe);
  fVar10 = (float)((ulonglong)*(undefined8 *)(param_3 + 2) >> 0x20) * fVar10 +
           (float)((ulonglong)*(undefined8 *)(param_3 + 6) >> 0x20) * fVar5 +
           param_3[0xb] * fVar6 + (float)((ulonglong)*(undefined8 *)(param_3 + 0xe) >> 0x20);
  auVar4._4_4_ = fVar8;
  auVar4._0_4_ = fVar7;
  auVar4._8_4_ = fVar9;
  auVar4._12_4_ = fVar10;
  auVar4 = rcpps(*(undefined1 (*) [16])(param_3 + 0xc),auVar4);
  fVar6 = auVar4._12_4_;
  fVar6 = (fVar6 + fVar6) - fVar6 * fVar10 * fVar6;
  *param_1 = CONCAT44(fVar8 * fVar6,fVar7 * fVar6);
  *(float *)(param_1 + 1) = fVar9 * fVar6;
  return param_1;
}

