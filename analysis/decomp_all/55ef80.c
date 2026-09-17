
ulonglong FUN__text__0055ef80(void)

{
  uint uVar1;
  ulonglong in_MM0;
  ulonglong uVar2;
  undefined8 uVar3;
  uint uVar4;
  uint uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  ulonglong uVar9;
  ulonglong uVar5;
  
  uVar2 = in_MM0 & DAT_0076075c;
  uVar6 = -(uint)(DAT_00760768 < (int)uVar2);
  uVar3 = PackedFloatingMUL(uVar2,(ulonglong)DAT_0076076c);
  uVar3 = PackedFloatingSUBR(uVar3,(ulonglong)DAT_0076076c);
  uVar7 = PackedFloatingReciprocalSQRAprox((ulonglong)DAT_0076075c,uVar3);
  uVar8 = PackedFloatingMUL(uVar7,uVar7);
  uVar1 = (uint)((int)uVar2 < DAT_007607a0);
  uVar4 = -uVar1;
  uVar5 = (ulonglong)uVar4;
  uVar8 = PackedFloatingReciprocalSQRIter1(uVar8,uVar3);
  uVar7 = PackedFloatingReciprocalIter2(uVar8,uVar7);
  uVar9 = PackedFloatingMUL(uVar7,uVar3);
  uVar2 = ~uVar5 & uVar9 | uVar2 & uVar4;
  uVar3 = PackedFloatingMUL(uVar2,uVar2);
  uVar8 = PackedFloatingMUL((ulonglong)DAT_007607a8,uVar3);
  uVar7 = PackedFloatingADD((ulonglong)DAT_007607b0,uVar3);
  uVar8 = PackedFloatingADD(uVar8,(ulonglong)DAT_007607a4);
  uVar8 = PackedFloatingMUL(uVar8,uVar3);
  uVar3 = PackedFloatingMUL(uVar3,uVar7);
  uVar3 = PackedFloatingADD(uVar3,(ulonglong)DAT_007607ac);
  uVar8 = PackedFloatingMUL(uVar8,uVar2);
  uVar7 = FloatingReciprocalAprox(uVar7,uVar3);
  uVar3 = PackedFloatingReciprocalIter1(uVar3,uVar7);
  uVar3 = PackedFloatingReciprocalIter2(uVar3,uVar7);
  uVar3 = PackedFloatingMUL(uVar3,uVar8);
  uVar2 = PackedFloatingADD(uVar2,uVar3);
  uVar3 = PackedFloatingADD(~uVar5 & (ulonglong)DAT_007607b8 ^ DAT_00760758 & in_MM0,
                            (ulonglong)DAT_007607b4);
  uVar2 = PackedFloatingADD(uVar2,~uVar5 & uVar2);
  uVar2 = PackedFloatingADD(uVar3,uVar2 | (ulonglong)(uVar1 * -0x80000000) ^ DAT_00760758 & in_MM0);
  return (ulonglong)(DAT_00760774 & uVar6) | ~(ulonglong)uVar6 & uVar2;
}

