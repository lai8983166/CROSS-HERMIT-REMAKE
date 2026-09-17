
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__00572070(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  float10 fVar2;
  int local_c;
  undefined4 local_8;
  
  local_8 = FUN__text__0057f0d0();
  if ((param_2._2_2_ & 0x7ff0) != 0x7ff0) {
    if ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) == _DAT_00592d98) {
      fVar2 = (float10)FUN__text__0057e260(4,0x25,param_1,param_2,-_DAT_007646c8,local_8);
      return fVar2;
    }
    FUN__text__0057ef50(param_1,param_2,&local_c);
    FUN__text__0057f0d0();
    return (float10)(local_c + -1);
  }
  iVar1 = FUN__text__0057eed0();
  if (0 < iVar1) {
    if (iVar1 < 3) {
      FUN__text__0057f0d0();
      return (float10)(double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1));
    }
    if (iVar1 == 3) {
      fVar2 = (float10)FUN__text__0057e190(0x25,param_1,param_2,local_8);
      return fVar2;
    }
  }
  fVar2 = (float10)FUN__text__0057e260(8,0x25,param_1,param_2,
                                       (double)CONCAT26(param_2._2_2_,
                                                        CONCAT24((undefined2)param_2,param_1)) +
                                       _DAT_005f9d58,local_8);
  return fVar2;
}

