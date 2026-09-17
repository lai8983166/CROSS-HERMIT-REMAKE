
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined *
FUN__text__00573130(char *param_1,undefined *param_2,undefined2 *param_3,undefined4 *param_4)

{
  int iVar1;
  undefined1 local_8c [136];
  
  if (param_1 == (char *)0x0) {
    param_2 = (undefined *)0x0;
  }
  else if ((*param_1 == 'C') && (param_1[1] == '\0')) {
    *param_2 = 0x43;
    param_2[1] = 0;
    if (param_3 != (undefined2 *)0x0) {
      *param_3 = 0;
      param_3[1] = 0;
      param_3[2] = 0;
    }
    if (param_4 != (undefined4 *)0x0) {
      *param_4 = 0;
    }
  }
  else {
    iVar1 = _strcmp("C",param_1);
    if ((iVar1 != 0) && (iVar1 = _strcmp("C",param_1), iVar1 != 0)) {
      iVar1 = FUN__text__00573320(local_8c,param_1);
      if (iVar1 != 0) {
        return (undefined *)0x0;
      }
      iVar1 = FUN__text__00581f90(local_8c,&DAT_0080a46c,local_8c);
      if (iVar1 == 0) {
        return (undefined *)0x0;
      }
      _DAT_0080a474 = (uint)DAT_0080a470;
      ___lc_lctostr(&DAT_00761aa0,local_8c);
      if (*param_1 == '\0') {
        FUN__text__0056cd90(&DAT_00761a1c,&DAT_00761aa0);
      }
      else {
        FUN__text__0056cd90(&DAT_00761a1c,param_1);
      }
    }
    if (param_3 != (undefined2 *)0x0) {
      FUN__text__0056d4d0(param_3,&DAT_0080a46c,6);
    }
    if (param_4 != (undefined4 *)0x0) {
      FUN__text__0056d4d0(param_4,&DAT_0080a474,4);
    }
    FUN__text__0056cd90(param_2,&DAT_00761aa0);
    param_2 = &DAT_00761aa0;
  }
  return param_2;
}

