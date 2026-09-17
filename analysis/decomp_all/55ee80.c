
ulonglong FUN__text__0055ee80(void)

{
  ulonglong in_MM0;
  ulonglong uVar1;
  undefined8 uVar2;
  ulonglong in_MM1;
  ulonglong uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  uint uVar7;
  uint uVar8;
  ulonglong uVar9;
  
  uVar9 = (DAT_00760758 & in_MM0) >> 1 | DAT_00760758 & in_MM1;
  uVar3 = in_MM1 & DAT_0076075c;
  uVar1 = in_MM0 & DAT_0076075c;
  uVar2 = PackedFloatingMAX(uVar1,uVar3);
  uVar7 = (uint)((int)uVar1 < (int)uVar3) * -0x80000000;
  uVar4 = PackedFloatingMIN(uVar3,uVar1);
  uVar5 = FloatingReciprocalAprox(uVar1,uVar2);
  uVar2 = PackedFloatingReciprocalIter1(uVar2,uVar5);
  uVar2 = PackedFloatingReciprocalIter2(uVar2,uVar5);
  uVar2 = PackedFloatingMUL(uVar2,uVar4);
  uVar4 = PackedFloatingMUL(uVar2,uVar2);
  uVar5 = PackedFloatingADD((ulonglong)DAT_00760790,uVar4);
  uVar6 = PackedFloatingMUL((ulonglong)DAT_0076079c,uVar4);
  uVar5 = PackedFloatingMUL(uVar5,uVar4);
  uVar6 = PackedFloatingADD(uVar6,(ulonglong)DAT_00760798);
  uVar5 = PackedFloatingADD(uVar5,(ulonglong)DAT_0076078c);
  uVar6 = PackedFloatingMUL(uVar6,uVar4);
  uVar5 = PackedFloatingMUL(uVar5,uVar4);
  uVar6 = PackedFloatingADD(uVar6,(ulonglong)DAT_00760794);
  uVar5 = PackedFloatingADD(uVar5,(ulonglong)DAT_00760788);
  uVar4 = PackedFloatingMUL(uVar4,uVar6);
  uVar4 = PackedFloatingMUL(uVar4,uVar2);
  uVar6 = FloatingReciprocalAprox((ulonglong)DAT_00760794,uVar5);
  uVar8 = (int)uVar9 << 1;
  uVar5 = PackedFloatingReciprocalIter1(uVar5,uVar6);
  uVar5 = PackedFloatingReciprocalIter2(uVar5,uVar6);
  uVar4 = PackedFloatingMUL(uVar4,uVar5);
  uVar1 = PackedFloatingADD(uVar4,uVar2);
  uVar2 = PackedFloatingSUB(~(ulonglong)(uint)((int)uVar7 >> 0x1f) &
                            (ulonglong)(uVar8 ^ DAT_007607b8),(ulonglong)DAT_007607b8);
  uVar1 = PackedFloatingADD(uVar1 | uVar8 ^ uVar7,uVar2);
  return uVar1 | DAT_00760758 & uVar9;
}

