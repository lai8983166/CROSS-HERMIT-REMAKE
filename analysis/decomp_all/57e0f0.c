
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__0057e0f0(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;
  undefined4 uVar2;
  float10 fVar3;
  
  uVar1 = FUN__text__00572560(param_1,param_2);
  if ((uVar1 & 0x90) == 0) {
    fVar3 = (float10)FUN__text__0057e170(param_1,param_2);
    if ((double)fVar3 == (double)CONCAT44(param_2,param_1)) {
      fVar3 = (float10)FUN__text__0057e170((double)CONCAT44(param_2,param_1) / _DAT_005fa640);
      if ((float10)(double)CONCAT44(param_2,param_1) / (float10)_DAT_005fa640 == fVar3) {
        uVar2 = 2;
      }
      else {
        uVar2 = 1;
      }
    }
    else {
      uVar2 = 0;
    }
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}

