
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00550711(uint param_1,undefined4 *param_2,undefined4 *param_3,undefined4 *param_4,
                        undefined4 *param_5,undefined8 *param_6)

{
  undefined4 uVar1;
  short sVar2;
  short sVar3;
  short sVar4;
  short sVar5;
  short sVar6;
  short sVar7;
  short sVar8;
  short sVar9;
  ushort uVar10;
  undefined7 uVar11;
  ulonglong uVar12;
  uint uVar13;
  byte bVar14;
  undefined2 uVar15;
  undefined8 uVar16;
  undefined2 uVar19;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined2 uVar22;
  undefined2 uVar23;
  undefined8 uVar20;
  undefined2 uVar24;
  undefined8 uVar21;
  undefined8 uVar25;
  undefined2 uVar27;
  undefined2 uVar28;
  undefined8 uVar26;
  undefined4 uVar29;
  undefined8 uVar30;
  
  param_1 = param_1 >> 2;
  do {
    uVar29 = *param_2;
    uVar1 = *param_3;
    uVar10 = (ushort)(((uint7)(byte)((uint)uVar29 >> 0x18) << 0x30) >> 0x28);
    uVar11 = CONCAT25(uVar10,CONCAT14((char)((uint)uVar29 >> 0x10),uVar29));
    uVar12 = (ulonglong)
             CONCAT41((int)(CONCAT34((int3)((uint7)uVar11 >> 0x20),uVar29) >> 0x18),
                      (char)((uint)uVar29 >> 8)) & 0xffffffff00ff;
    bVar14 = (byte)uVar29;
    uVar29 = *param_4;
    uVar17 = psubsw((ulonglong)
                    CONCAT52((int5)(CONCAT43((int)(CONCAT34((int3)(CONCAT25((short)(((uint7)(byte)((
                                                  uint)uVar1 >> 0x18) << 0x30) >> 0x28),
                                                  CONCAT14((char)((uint)uVar1 >> 0x10),uVar1)) >>
                                                  0x20),uVar1) >> 0x18),
                                             CONCAT12((char)((uint)uVar1 >> 8),(short)uVar1)) >>
                                   0x10),(short)uVar1) & 0xffffffff00ff00ff,_PTR_DAT_0075fde8);
    uVar20 = psubsw((ulonglong)
                    CONCAT52(CONCAT41((int)(CONCAT34((int3)(CONCAT25((short)(((uint7)(byte)((uint)
                                                  uVar29 >> 0x18) << 0x30) >> 0x28),
                                                  CONCAT14((char)((uint)uVar29 >> 0x10),uVar29)) >>
                                                  0x20),uVar29) >> 0x18),(char)((uint)uVar29 >> 8)),
                             (ushort)(byte)uVar29) & 0xffffffff00ffffff,_PTR_DAT_0075fde8);
    uVar22 = (undefined2)((ulonglong)uVar20 >> 0x10);
    uVar19 = (undefined2)((ulonglong)uVar17 >> 0x10);
    uVar18 = pmaddwd(CONCAT44(CONCAT22(uVar22,uVar19),CONCAT22((short)uVar20,(short)uVar17)),
                     _DAT_0075fdf0);
    uVar16 = psllw(CONCAT62((int6)uVar12,(ushort)bVar14),8);
    uVar27 = (undefined2)((ulonglong)uVar17 >> 0x20);
    uVar23 = (undefined2)((ulonglong)uVar20 >> 0x20);
    uVar28 = (undefined2)((ulonglong)uVar17 >> 0x30);
    uVar24 = (undefined2)((ulonglong)uVar20 >> 0x30);
    uVar26 = pmaddwd(CONCAT26(uVar24,CONCAT24(uVar28,CONCAT22(uVar23,uVar27))),_DAT_0075fdf0);
    uVar15 = (undefined2)uVar12;
    uVar20 = pmaddwd(CONCAT44(CONCAT22(uVar15,uVar22),(uint)CONCAT12(bVar14,(short)uVar20)),
                     _DAT_0075fdf8);
    uVar25 = pmaddwd(CONCAT44(CONCAT22(uVar15,uVar19),(uint)CONCAT12(bVar14,(short)uVar17)),
                     _DAT_0075fe00);
    uVar15 = (undefined2)((uint7)uVar11 >> 0x20);
    uVar10 = uVar10 >> 8;
    uVar30 = pmaddwd(CONCAT26(uVar10,CONCAT24(uVar28,CONCAT22(uVar15,uVar27))),_DAT_0075fe00);
    uVar17 = pmaddwd(CONCAT26(uVar10,CONCAT24(uVar24,CONCAT22(uVar15,uVar23))),_DAT_0075fdf8);
    uVar29 = *param_5;
    uVar15 = CONCAT11((char)((uint)(undefined4)DAT_0080a3a0 >> 0x18),(char)((uint)uVar29 >> 0x18));
    uVar13 = (uint)(undefined4)DAT_0080a3a0 >> 0x10;
    uVar21 = packssdw(CONCAT44((int)((int)uVar18 + (uint)(ushort)uVar16) >> 8,(int)uVar20 >> 8),
                      CONCAT44(CONCAT22((short)(undefined4)DAT_0080a3a0,
                                        CONCAT11((char)(undefined4)DAT_0080a3a0,(char)uVar29)),
                               (int)uVar25 >> 8));
    uVar18 = packssdw(CONCAT44((int)((int)((ulonglong)uVar18 >> 0x20) +
                                    (uint)(ushort)((ulonglong)uVar16 >> 0x10)) >> 8,
                               (int)((longlong)uVar20 >> 0x28)),
                      CONCAT44(CONCAT22((short)((uint)(undefined4)DAT_0080a3a0 >> 0x10),
                                        CONCAT11((char)((uint)(undefined4)DAT_0080a3a0 >> 8),
                                                 (char)((uint)uVar29 >> 8))),
                               (int)((longlong)uVar25 >> 0x28)));
    sVar2 = (short)uVar21;
    sVar3 = (short)((ulonglong)uVar21 >> 0x10);
    sVar4 = (short)((ulonglong)uVar21 >> 0x20);
    sVar5 = (short)((ulonglong)uVar21 >> 0x30);
    sVar6 = (short)uVar18;
    sVar7 = (short)((ulonglong)uVar18 >> 0x10);
    sVar8 = (short)((ulonglong)uVar18 >> 0x20);
    sVar9 = (short)((ulonglong)uVar18 >> 0x30);
    *param_6 = CONCAT17((0 < sVar9) * (sVar9 < 0x100) * (char)((ulonglong)uVar18 >> 0x30) -
                        (0xff < sVar9),
                        CONCAT16((0 < sVar8) * (sVar8 < 0x100) * (char)((ulonglong)uVar18 >> 0x20) -
                                 (0xff < sVar8),
                                 CONCAT15((0 < sVar7) * (sVar7 < 0x100) *
                                          (char)((ulonglong)uVar18 >> 0x10) - (0xff < sVar7),
                                          CONCAT14((0 < sVar6) * (sVar6 < 0x100) * (char)uVar18 -
                                                   (0xff < sVar6),
                                                   CONCAT13((0 < sVar5) * (sVar5 < 0x100) *
                                                            (char)((ulonglong)uVar21 >> 0x30) -
                                                            (0xff < sVar5),
                                                            CONCAT12((0 < sVar4) * (sVar4 < 0x100) *
                                                                     (char)((ulonglong)uVar21 >>
                                                                           0x20) - (0xff < sVar4),
                                                                     CONCAT11((0 < sVar3) *
                                                                              (sVar3 < 0x100) *
                                                                              (char)((ulonglong)
                                                                                     uVar21 >> 0x10)
                                                                              - (0xff < sVar3),
                                                                              (0 < sVar2) *
                                                                              (sVar2 < 0x100) *
                                                                              (char)uVar21 -
                                                                              (0xff < sVar2))))))));
    uVar29 = CONCAT22((short)DAT_0080a3a0._4_4_,
                      (short)(CONCAT35(CONCAT21(uVar15,(char)uVar13),
                                       CONCAT14((char)((uint)uVar29 >> 0x10),uVar29)) >> 0x20));
    param_2 = param_2 + 1;
    param_3 = param_3 + 1;
    uVar18 = packssdw(CONCAT44((int)((int)uVar26 + (uint)(ushort)((ulonglong)uVar16 >> 0x20)) >> 8,
                               (int)uVar17 >> 8),CONCAT44(uVar29,(int)uVar30 >> 8));
    param_4 = param_4 + 1;
    uVar16 = packssdw(CONCAT44((int)((int)((ulonglong)uVar26 >> 0x20) +
                                    (uint)(ushort)((ulonglong)uVar16 >> 0x30)) >> 8,
                               (int)((longlong)uVar17 >> 0x28)),
                      CONCAT44((int)(CONCAT26((short)((uint)DAT_0080a3a0._4_4_ >> 0x10),
                                              CONCAT24(uVar15,uVar29)) >> 0x20),
                               (int)((longlong)uVar30 >> 0x28)));
    sVar2 = (short)uVar18;
    sVar3 = (short)((ulonglong)uVar18 >> 0x10);
    sVar4 = (short)((ulonglong)uVar18 >> 0x20);
    sVar5 = (short)((ulonglong)uVar18 >> 0x30);
    sVar6 = (short)uVar16;
    sVar7 = (short)((ulonglong)uVar16 >> 0x10);
    sVar8 = (short)((ulonglong)uVar16 >> 0x20);
    sVar9 = (short)((ulonglong)uVar16 >> 0x30);
    param_5 = param_5 + 1;
    param_6[1] = CONCAT17((0 < sVar9) * (sVar9 < 0x100) * (char)((ulonglong)uVar16 >> 0x30) -
                          (0xff < sVar9),
                          CONCAT16((0 < sVar8) * (sVar8 < 0x100) * (char)((ulonglong)uVar16 >> 0x20)
                                   - (0xff < sVar8),
                                   CONCAT15((0 < sVar7) * (sVar7 < 0x100) *
                                            (char)((ulonglong)uVar16 >> 0x10) - (0xff < sVar7),
                                            CONCAT14((0 < sVar6) * (sVar6 < 0x100) * (char)uVar16 -
                                                     (0xff < sVar6),
                                                     CONCAT13((0 < sVar5) * (sVar5 < 0x100) *
                                                              (char)((ulonglong)uVar18 >> 0x30) -
                                                              (0xff < sVar5),
                                                              CONCAT12((0 < sVar4) * (sVar4 < 0x100)
                                                                       * (char)((ulonglong)uVar18 >>
                                                                               0x20) -
                                                                       (0xff < sVar4),
                                                                       CONCAT11((0 < sVar3) *
                                                                                (sVar3 < 0x100) *
                                                                                (char)((ulonglong)
                                                                                       uVar18 >>
                                                                                      0x10) -
                                                                                (0xff < sVar3),
                                                                                (0 < sVar2) *
                                                                                (sVar2 < 0x100) *
                                                                                (char)uVar18 -
                                                                                (0xff < sVar2)))))))
                         );
    param_1 = param_1 - 1;
    param_6 = param_6 + 2;
  } while (param_1 != 0);
  return;
}

