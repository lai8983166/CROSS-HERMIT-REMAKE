
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__005564fb(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3,uint param_4)

{
  uint uVar1;
  uint uVar2;
  undefined8 uVar3;
  ulonglong uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  ulonglong uVar8;
  uint uVar9;
  uint uVar10;
  
  FastExitMediaState();
  uVar3 = PackedFloatingMUL(*param_2,*param_3);
  uVar5 = PackedFloatingMUL(param_2[1],param_3[1]);
  uVar5 = PackedFloatingADD(uVar3,uVar5);
  uVar3 = PackedFloatingSUB((ulonglong)DAT_005d3568,(ulonglong)param_4);
  uVar1 = (uint)uVar3;
  uVar4 = PackedFloatingAccumulate(uVar5,uVar5);
  uVar8 = PackedFloatingCompareGE(0,uVar4);
  uVar8 = uVar8 & _DAT_005d35b0;
  uVar4 = uVar4 ^ uVar8;
  uVar5 = PackedFloatingCompareGE(DAT_005d35c8,uVar4);
  uVar3 = PackedFloatingMUL(uVar4,uVar4);
  uVar3 = PackedFloatingSUBR(uVar3,CONCAT44(_UNK_005d356c,DAT_005d3568));
  if ((int)uVar5 != 0) {
    uVar6 = PackedFloatingReciprocalSQRAprox((ulonglong)param_4,uVar3);
    uVar5 = PackedFloatingMUL(uVar6,uVar6);
    uVar3 = PackedFloatingReciprocalSQRIter1(uVar3,uVar5);
    uVar6 = PackedFloatingReciprocalIter2(uVar3,uVar6);
    uVar3 = FloatingReciprocalAprox(uVar5,uVar6);
    uVar5 = PackedFloatingReciprocalIter1(uVar6,uVar3);
    PackedFloatingReciprocalIter2(uVar5,uVar3);
    uVar9 = (uint)uVar6;
    uVar3 = FUN__text__0055ee80();
    uVar10 = (uint)uVar3;
    PackedFloatingMUL(uVar3,(ulonglong)param_4);
    uVar2 = FUN__text__0055f680(uVar1,uVar9,uVar10);
    PackedFloatingMUL((ulonglong)uVar10,(ulonglong)uVar1);
    uVar3 = FUN__text__0055f680();
    uVar8 = uVar8 & 0xffffffff;
    uVar3 = PackedFloatingMUL(uVar3,(ulonglong)uVar9);
    uVar1 = (uint)uVar3;
    uVar3 = PackedFloatingMUL((ulonglong)uVar2,(ulonglong)uVar9);
    param_4 = (uint)uVar3;
  }
  param_4 = param_4 ^ (uint)uVar8;
  uVar5 = CONCAT44(param_4,param_4);
  uVar3 = PackedFloatingMUL(CONCAT44(uVar1,uVar1),*param_2);
  uVar6 = PackedFloatingMUL(uVar5,*param_3);
  uVar7 = PackedFloatingMUL(CONCAT44(uVar1,uVar1),param_2[1]);
  uVar5 = PackedFloatingMUL(uVar5,param_3[1]);
  uVar3 = PackedFloatingADD(uVar3,uVar6);
  uVar5 = PackedFloatingADD(uVar7,uVar5);
  *param_1 = uVar3;
  param_1[1] = uVar5;
  FastExitMediaState();
  return;
}

