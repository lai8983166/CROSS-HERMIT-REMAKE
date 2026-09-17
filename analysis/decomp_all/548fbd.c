
undefined4 __thiscall FUN__text__00548fbd(int *param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  int iVar2;
  
  if (param_1[1] == 0) {
    if (param_2 != (undefined4 *)0x0) {
      *param_2 = 0;
    }
    uVar1 = 0x80004005;
    param_1[3] = -0x7fffbffb;
  }
  else {
    iVar2 = param_1[1] + -1;
    param_1[1] = iVar2;
    if (param_2 != (undefined4 *)0x0) {
      *param_2 = *(undefined4 *)(*param_1 + iVar2 * 4);
    }
    uVar1 = 0;
  }
  return uVar1;
}

