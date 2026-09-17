
undefined4 __thiscall FUN__text__00587b90(undefined4 param_1,int *param_2)

{
  undefined4 uVar1;
  int iVar2;
  
  if (DAT_00764ed4 == 0) {
    return 0;
  }
  if ((param_2[5] != DAT_00764f68) || (param_2[5] != DAT_00764f78)) {
    if (DAT_0080a6c0 == 0) {
      FUN__text__00587e90(1,1,param_2[5],4,1,0,0,2,0,0,0,param_1);
      FUN__text__00587e90(0,1,param_2[5],10,5,0,0,2,0,0,0);
    }
    else {
      if (DAT_0080a760 == 0) {
        FUN__text__00587e90(1,1,param_2[5],DAT_0080a762,DAT_0080a766,DAT_0080a764,0,DAT_0080a768,
                            DAT_0080a76a,DAT_0080a76c,DAT_0080a76e,param_1);
      }
      else {
        FUN__text__00587e90(1,0,param_2[5],DAT_0080a762,0,0,DAT_0080a766,DAT_0080a768,DAT_0080a76a,
                            DAT_0080a76c,DAT_0080a76e,param_1);
      }
      if (DAT_0080a70c == 0) {
        FUN__text__00587e90(0,1,param_2[5],DAT_0080a70e,DAT_0080a712,DAT_0080a710,0,DAT_0080a714,
                            DAT_0080a716,DAT_0080a718,DAT_0080a71a,param_1);
      }
      else {
        FUN__text__00587e90(0,0,param_2[5],DAT_0080a70e,0,0,DAT_0080a712,DAT_0080a714,DAT_0080a716,
                            DAT_0080a718,DAT_0080a71a,param_1);
      }
    }
  }
  if (DAT_00764f6c < DAT_00764f7c) {
    if ((param_2[7] < DAT_00764f6c) || (DAT_00764f7c < param_2[7])) {
      return 0;
    }
    if ((DAT_00764f6c < param_2[7]) && (param_2[7] < DAT_00764f7c)) {
      return 1;
    }
  }
  else {
    if ((param_2[7] < DAT_00764f7c) || (DAT_00764f6c < param_2[7])) {
      return 1;
    }
    if ((DAT_00764f7c < param_2[7]) && (param_2[7] < DAT_00764f6c)) {
      return 0;
    }
  }
  iVar2 = (*param_2 + param_2[1] * 0x3c + param_2[2] * 0xe10) * 1000;
  if (param_2[7] == DAT_00764f6c) {
    if (iVar2 < DAT_00764f70) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  else if (iVar2 < DAT_00764f80) {
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

