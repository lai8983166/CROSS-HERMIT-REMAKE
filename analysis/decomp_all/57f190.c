
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__0057f190(undefined4 param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  float10 fVar2;
  double dVar3;
  undefined4 uVar4;
  int local_38;
  int local_18;
  int local_14;
  undefined4 local_10;
  double local_c;
  
  local_10 = FUN__text__0057f0d0();
  if ((param_2._2_2_ & 0x7ff0) == 0x7ff0) {
    iVar1 = FUN__text__0057eed0();
    if (0 < iVar1) {
      if (iVar1 < 3) {
        FUN__text__0057f0d0();
        return (float10)(double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1));
      }
      if (iVar1 == 3) {
        fVar2 = (float10)FUN__text__0057e1f0(0x19,param_1,param_2,(double)param_3,local_10);
        return fVar2;
      }
    }
    fVar2 = (float10)FUN__text__0057e320(8,0x19,param_1,param_2,(double)param_3,
                                         (double)CONCAT26(param_2._2_2_,
                                                          CONCAT24((undefined2)param_2,param_1)) +
                                         _DAT_005f9d58,local_10);
    return fVar2;
  }
  if ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) == _DAT_00592d98) {
    FUN__text__0057f0d0();
    return (float10)(double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1));
  }
  fVar2 = (float10)FUN__text__0057ef50(param_1,param_2,&local_14);
  dVar3 = (double)fVar2;
  if (param_3 < 0) {
    local_38 = -param_3;
  }
  else {
    local_38 = param_3;
  }
  if (local_38 <= 0x7fffffff) {
    local_18 = local_14 + param_3;
  }
  else {
    local_18 = param_3;
  }
  if (0xa00 < local_18) {
    uVar4 = local_10;
    dVar3 = __copysign((double)CONCAT44(DAT_007646cc,DAT_007646c8),dVar3);
    fVar2 = (float10)FUN__text__0057e320(0x11,0x19,param_1,param_2,(double)param_3,dVar3,uVar4);
    return fVar2;
  }
  if (0x400 < local_18) {
    fVar2 = (float10)FUN__text__0057ede0(dVar3,local_18 + -0x600);
    local_c = (double)fVar2;
    fVar2 = (float10)FUN__text__0057e320(0x11,0x19,param_1,param_2,(double)param_3,local_c,local_10)
    ;
    return fVar2;
  }
  if (local_18 < -0x9fd) {
    fVar2 = (float10)FUN__text__0057e320(0x12,0x19,param_1,param_2,(double)param_3,
                                         dVar3 * _DAT_00592d98,local_10);
    return fVar2;
  }
  if (local_18 < -0x3fd) {
    fVar2 = (float10)FUN__text__0057ede0(dVar3,local_18 + 0x600);
    local_c = (double)fVar2;
    fVar2 = (float10)FUN__text__0057e320(0x12,0x19,param_1,param_2,(double)param_3,local_c,local_10)
    ;
    return fVar2;
  }
  fVar2 = (float10)FUN__text__0057ede0(dVar3,local_18);
  local_c = (double)fVar2;
  FUN__text__0057f0d0();
  return (float10)local_c;
}

