
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__00571dc0(undefined4 param_1,undefined4 param_2)

{
  double dVar1;
  uint uVar2;
  int iVar3;
  float10 fVar4;
  
  uVar2 = FUN__text__0057f0d0();
  if ((param_2._2_2_ & 0x7ff0) != 0x7ff0) {
    fVar4 = (float10)FUN__text__0057e170();
    dVar1 = (double)fVar4;
    if (dVar1 == (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1))) {
      FUN__text__0057f0d0();
      return (float10)dVar1;
    }
    if ((uVar2 & 0x20) != 0) {
      FUN__text__0057f0d0();
      return (float10)dVar1;
    }
    fVar4 = (float10)FUN__text__0057e260(0x10,0xb,param_1,param_2,dVar1,uVar2);
    return fVar4;
  }
  iVar3 = FUN__text__0057eed0();
  if (0 < iVar3) {
    if (iVar3 < 3) {
      FUN__text__0057f0d0();
      return (float10)(double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1));
    }
    if (iVar3 == 3) {
      fVar4 = (float10)FUN__text__0057e190(0xb,param_1,param_2,uVar2);
      return fVar4;
    }
  }
  fVar4 = (float10)FUN__text__0057e260(8,0xb,param_1,param_2,
                                       (double)CONCAT26(param_2._2_2_,
                                                        CONCAT24((undefined2)param_2,param_1)) +
                                       _DAT_005f9d58,uVar2);
  return fVar4;
}

