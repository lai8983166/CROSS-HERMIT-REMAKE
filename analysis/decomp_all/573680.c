
undefined4 FUN__text__00573680(int param_1,uint param_2)

{
  undefined4 uVar1;
  
  if ((param_1 < 0) || (2 < param_1)) {
    uVar1 = 0xffffffff;
  }
  else if (param_2 == 0xffffffff) {
    uVar1 = *(undefined4 *)(&DAT_00761b74 + param_1 * 4);
  }
  else if ((param_2 & 0xfffffff8) == 0) {
    uVar1 = *(undefined4 *)(&DAT_00761b74 + param_1 * 4);
    *(uint *)(&DAT_00761b74 + param_1 * 4) = param_2;
  }
  else {
    uVar1 = 0xffffffff;
  }
  return uVar1;
}

