
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0054caca(uint param_1,int param_2,int param_3)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  char *pcVar4;
  
  uVar2 = param_1;
  uVar1 = *(uint *)(param_1 + 0x58);
  if ((uVar1 & 1) == 0) {
    FUN__text__0054381d(param_1,"Missing IHDR before sRGB");
  }
  else {
    if ((uVar1 & 4) != 0) {
      pcVar4 = "Invalid sRGB after IDAT";
      goto LAB__text__0054caf0;
    }
    if ((uVar1 & 2) == 0) {
      if ((param_2 != 0) && ((*(byte *)(param_2 + 9) & 8) != 0)) {
        pcVar4 = "Duplicate sRGB chunk";
        goto LAB__text__0054caf0;
      }
    }
    else {
      FUN__text__0054383b(param_1,"Out of place sRGB chunk");
    }
  }
  if (param_3 == 1) {
    FUN__text__0054bcf9(uVar2,(int)&param_1 + 3,1);
    iVar3 = FUN__text__0054c5c9(uVar2,0);
    if (iVar3 != 0) {
      return;
    }
    uVar1 = param_1 >> 0x18;
    if (3 < uVar1) {
      FUN__text__0054383b(uVar2,"Unknown sRGB intent");
      return;
    }
    if (((*(byte *)(param_2 + 8) & 1) != 0) &&
       ((float)_DAT_005d3950 <
        ABS((*(float *)(uVar2 + 0x130) * _DAT_005d39e0 + (float)_DAT_005d0dd0) -
            (float)_DAT_005d3958))) {
      FUN__text__0054383b(uVar2,"Ignoring incorrect gAMA value when sRGB is also present");
    }
    FUN__text__005464e5(uVar2,param_2,uVar1);
    return;
  }
  pcVar4 = "Incorrect sRGB chunk length";
LAB__text__0054caf0:
  FUN__text__0054383b(uVar2,pcVar4);
  FUN__text__0054c5c9(uVar2,param_3);
  return;
}

