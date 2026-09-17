
int FUN__text__00528a7b(int param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5,
                       int *param_6,undefined4 param_7,undefined4 param_8,undefined4 param_9)

{
  int iVar1;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  int local_5c;
  int local_58;
  int local_50;
  int iStack_4c;
  int iStack_48;
  int iStack_44;
  undefined4 local_38;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  FUN__text__0052b0a9();
  if (((param_1 == 0) || (param_4 == 0)) || (param_5 == 0)) {
LAB__text__00528aea:
    iVar1 = -0x7789f794;
  }
  else {
    iVar1 = FUN__text__0052d4bb(param_4,param_5,param_9,1);
    if (iVar1 < 0) goto LAB__text__00528aef;
    if (param_6 == (int *)0x0) {
      local_14 = local_50;
      local_10 = iStack_4c;
      local_c = iStack_48;
      local_8 = iStack_44;
    }
    else {
      local_14 = *param_6;
      local_10 = param_6[1];
      local_c = param_6[2];
      local_8 = param_6[3];
      if ((((local_14 < 0) || (local_5c < local_c)) ||
          ((local_c < local_14 || ((local_10 < 0 || (local_58 < local_8)))))) ||
         (local_8 < local_10)) goto LAB__text__00528aea;
    }
    iVar1 = FUN__text__00526e9f(param_1,param_2,param_3,local_64,local_68,local_38,local_60,
                                &local_14,param_7,param_8);
    if (-1 < iVar1) {
      iVar1 = 0;
    }
  }
LAB__text__00528aef:
  FUN__text__0052b0c2();
  return iVar1;
}

