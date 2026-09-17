
undefined4 FUN__text__00578a80(uint param_1)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  uint local_8;
  
  if (DAT_0080ab2c == 3) {
    if (param_1 < 0x3f9) {
      DAT_0080ab4c = param_1;
      uVar1 = 1;
    }
    else {
      uVar1 = 0;
    }
  }
  else if (DAT_0080ab2c == 2) {
    uVar3 = param_1 + 0xf & 0xfffffff0;
    if (uVar3 < 0x781) {
      uVar1 = 1;
      DAT_0076415c = uVar3;
    }
    else {
      uVar1 = 0;
    }
  }
  else {
    if ((DAT_0080ab2c == 1) && (param_1 != 0)) {
      FUN__text__0057b740(&local_8);
      if ((local_8 & 0xff) < 6) {
        uVar3 = param_1 + 0xf & 0xfffffff0;
        if ((uVar3 < 0x781) && (iVar2 = FUN__text__0057a860(), iVar2 != 0)) {
          DAT_0076415c = uVar3;
          DAT_0080ab2c = 2;
          return 1;
        }
      }
      else if ((param_1 < 0x3f9) && (iVar2 = ___sbh_heap_init(param_1), iVar2 != 0)) {
        DAT_0080ab2c = 3;
        DAT_0080ab4c = param_1;
        return 1;
      }
    }
    uVar1 = 0;
  }
  return uVar1;
}

