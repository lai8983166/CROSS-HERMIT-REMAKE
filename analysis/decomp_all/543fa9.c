
void FUN__text__00543fa9(undefined4 param_1,undefined4 *param_2,undefined4 *param_3,int param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  if (param_2 == (undefined4 *)0x0) {
    if (param_3 != (undefined4 *)0x0) {
      for (; param_4 != 0; param_4 = param_4 + -1) {
        FUN__text__00543c02(param_1,0,*param_3);
        param_3 = param_3 + 1;
      }
    }
  }
  else if (param_3 == (undefined4 *)0x0) {
    for (; param_4 != 0; param_4 = param_4 + -1) {
      FUN__text__00543c02(param_1,*param_2,0);
      param_2 = param_2 + 1;
    }
  }
  else {
    for (; param_4 != 0; param_4 = param_4 + -1) {
      uVar1 = *param_3;
      uVar2 = *param_2;
      param_2 = param_2 + 1;
      param_3 = param_3 + 1;
      FUN__text__00543c02(param_1,uVar2,uVar1);
    }
  }
  return;
}

