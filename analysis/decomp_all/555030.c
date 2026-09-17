
undefined8 * FUN__text__00555030(undefined8 *param_1,float *param_2,undefined8 *param_3)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  undefined1 auVar4 [16];
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  float fVar26;
  float fVar27;
  float fVar28;
  float fVar29;
  float fVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  float fVar34;
  float fVar35;
  float fVar36;
  float fVar37;
  float fVar38;
  float fVar39;
  float fVar40;
  float fVar41;
  float fVar42;
  float fVar43;
  float fVar44;
  float fVar45;
  float fVar46;
  float fVar47;
  float fVar48;
  float fVar49;
  float fVar50;
  float fVar51;
  
  fVar32 = (float)param_3[5];
  fVar33 = (float)((ulonglong)param_3[5] >> 0x20);
  fVar34 = (float)param_3[7];
  fVar35 = (float)((ulonglong)param_3[7] >> 0x20);
  fVar24 = (float)param_3[4];
  fVar26 = (float)((ulonglong)param_3[4] >> 0x20);
  fVar14 = (float)*param_3;
  fVar18 = (float)((ulonglong)*param_3 >> 0x20);
  fVar28 = (float)param_3[6];
  fVar30 = (float)((ulonglong)param_3[6] >> 0x20);
  fVar20 = (float)param_3[2];
  fVar22 = (float)((ulonglong)param_3[2] >> 0x20);
  fVar1 = (float)param_3[1];
  fVar5 = (float)((ulonglong)param_3[1] >> 0x20);
  fVar8 = (float)param_3[3];
  fVar11 = (float)((ulonglong)param_3[3] >> 0x20);
  fVar36 = fVar33 * fVar1;
  fVar39 = fVar35 * fVar8;
  fVar42 = fVar5 * fVar32;
  fVar45 = fVar11 * fVar34;
  fVar37 = fVar26 * fVar1;
  fVar40 = fVar30 * fVar8;
  fVar43 = fVar18 * fVar32;
  fVar46 = fVar22 * fVar34;
  fVar48 = fVar18 * fVar33;
  fVar49 = fVar22 * fVar35;
  fVar50 = fVar26 * fVar5;
  fVar51 = fVar30 * fVar11;
  fVar2 = (fVar32 * fVar49 +
          ((fVar33 * fVar40 + (fVar26 * fVar45 - fVar26 * fVar39)) - fVar33 * fVar46)) -
          fVar32 * fVar51;
  fVar6 = (fVar34 * fVar48 +
          ((fVar35 * fVar37 + (fVar30 * fVar42 - fVar30 * fVar36)) - fVar35 * fVar43)) -
          fVar34 * fVar50;
  fVar9 = (fVar1 * fVar51 +
          ((fVar5 * fVar46 + (fVar18 * fVar39 - fVar18 * fVar45)) - fVar5 * fVar40)) -
          fVar1 * fVar49;
  fVar12 = (fVar8 * fVar50 +
           ((fVar11 * fVar43 + (fVar22 * fVar36 - fVar22 * fVar42)) - fVar11 * fVar37)) -
           fVar8 * fVar48;
  fVar15 = fVar14 * fVar2;
  fVar19 = fVar20 * fVar6;
  fVar21 = fVar24 * fVar9;
  fVar23 = fVar28 * fVar12;
  fVar16 = fVar21 + fVar15;
  fVar17 = fVar23 + fVar19 + fVar16;
  fVar38 = fVar14 * fVar26;
  fVar41 = fVar20 * fVar30;
  fVar44 = fVar24 * fVar18;
  fVar47 = fVar28 * fVar22;
  fVar25 = fVar33 * fVar14;
  fVar27 = fVar35 * fVar20;
  fVar29 = fVar5 * fVar24;
  fVar31 = fVar11 * fVar28;
  fVar3 = fVar14 * fVar32;
  fVar7 = fVar20 * fVar34;
  fVar10 = fVar24 * fVar1;
  fVar13 = fVar28 * fVar8;
  if (fVar17 != 0.0) {
    if (param_2 != (float *)0x0) {
      *param_2 = fVar17;
    }
    auVar4._4_4_ = fVar16;
    auVar4._0_4_ = fVar17;
    auVar4._8_4_ = fVar19 + fVar23;
    auVar4._12_4_ = fVar15 + fVar21;
    auVar4 = rcpss(auVar4,auVar4);
    fVar15 = auVar4._0_4_;
    fVar15 = (fVar15 + fVar15) - fVar17 * fVar15 * fVar15;
    *param_1 = CONCAT44(fVar6 * fVar15,fVar2 * fVar15);
    param_1[1] = CONCAT44(fVar12 * fVar15,fVar9 * fVar15);
    param_1[2] = CONCAT44(((((fVar36 * fVar28 - fVar42 * fVar28) - fVar25 * fVar34) +
                            fVar29 * fVar34 + fVar35 * fVar3) - fVar35 * fVar10) * fVar15,
                          ((((fVar39 * fVar24 - fVar45 * fVar24) - fVar27 * fVar32) +
                            fVar31 * fVar32 + fVar33 * fVar7) - fVar33 * fVar13) * fVar15);
    param_1[3] = CONCAT44(((((fVar42 * fVar20 - fVar36 * fVar20) - fVar29 * fVar8) + fVar25 * fVar8
                           + fVar11 * fVar10) - fVar11 * fVar3) * fVar15,
                          ((((fVar45 * fVar14 - fVar39 * fVar14) - fVar31 * fVar1) + fVar27 * fVar1
                           + fVar5 * fVar13) - fVar5 * fVar7) * fVar15);
    param_1[4] = CONCAT44(((fVar30 * fVar25 +
                           (fVar35 * fVar44 -
                           (fVar35 * fVar38 + (fVar48 * fVar28 - fVar50 * fVar28)))) -
                          fVar30 * fVar29) * fVar15,
                          ((fVar26 * fVar27 +
                           (fVar33 * fVar47 -
                           (fVar33 * fVar41 + (fVar49 * fVar24 - fVar51 * fVar24)))) -
                          fVar26 * fVar31) * fVar15);
    param_1[5] = CONCAT44(((fVar22 * fVar29 +
                           (fVar11 * fVar38 -
                           (fVar11 * fVar44 + (fVar50 * fVar20 - fVar48 * fVar20)))) -
                          fVar22 * fVar25) * fVar15,
                          ((fVar18 * fVar31 +
                           (fVar5 * fVar41 - (fVar5 * fVar47 + (fVar51 * fVar14 - fVar49 * fVar14)))
                           ) - fVar18 * fVar27) * fVar15);
    param_1[6] = CONCAT44(fVar15 * (fVar30 * fVar10 +
                                   (((fVar38 * fVar34 - (fVar37 * fVar28 - fVar43 * fVar28)) -
                                    fVar34 * fVar44) - fVar3 * fVar30)),
                          fVar15 * (fVar26 * fVar13 +
                                   (((fVar41 * fVar32 - (fVar40 * fVar24 - fVar46 * fVar24)) -
                                    fVar32 * fVar47) - fVar7 * fVar26)));
    param_1[7] = CONCAT44(fVar15 * (fVar22 * fVar3 +
                                   (((fVar44 * fVar8 - (fVar43 * fVar20 - fVar37 * fVar20)) -
                                    fVar8 * fVar38) - fVar10 * fVar22)),
                          fVar15 * (fVar18 * fVar7 +
                                   (((fVar47 * fVar1 - (fVar46 * fVar14 - fVar40 * fVar14)) -
                                    fVar1 * fVar41) - fVar13 * fVar18)));
    return param_1;
  }
  return (undefined8 *)0x0;
}

