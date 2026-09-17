
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0054c9bf(int param_1,int param_2,int param_3)

{
  uint uVar1;
  float fVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  
  iVar4 = param_2;
  iVar3 = param_1;
  uVar1 = *(uint *)(param_1 + 0x58);
  if ((uVar1 & 1) == 0) {
    FUN__text__0054381d(param_1,"Missing IHDR before gAMA");
  }
  else {
    if ((uVar1 & 4) != 0) goto LAB__text__0054c9f0;
    if ((uVar1 & 2) == 0) {
      if (((param_2 != 0) && ((*(uint *)(param_2 + 8) & 1) != 0)) &&
         ((*(uint *)(param_2 + 8) & 0x800) == 0)) goto LAB__text__0054c9f0;
    }
    else {
      FUN__text__0054383b(param_1,"Out of place gAMA chunk");
    }
  }
  if (param_3 == 4) {
    FUN__text__0054bcf9(iVar3,&param_1,4);
    iVar5 = FUN__text__0054c5c9(iVar3,0);
    if (iVar5 != 0) {
      return;
    }
    iVar5 = FUN__text__0054bcc3();
    if (iVar5 == 0) {
      return;
    }
    if ((*(uint *)(iVar4 + 8) & 0x800) != 0) {
      fVar2 = (float)iVar5;
      if (iVar5 < 0) {
        fVar2 = fVar2 + _DAT_005d0a44;
      }
      if ((float)_DAT_005d3950 < ABS(fVar2 - (float)_DAT_005d3958)) {
        FUN__text__0054383b(iVar3,"Ignoring incorrect gAMA value when sRGB is also present");
        return;
      }
    }
    fVar2 = (float)iVar5;
    if (iVar5 < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
    }
    fVar2 = fVar2 * _DAT_005d0e08;
    *(float *)(iVar3 + 0x130) = fVar2;
    FUN__text__005463ea(iVar3,iVar4,(double)fVar2);
    return;
  }
LAB__text__0054c9f0:
  FUN__text__0054383b(iVar3);
  FUN__text__0054c5c9(iVar3,param_3);
  return;
}

