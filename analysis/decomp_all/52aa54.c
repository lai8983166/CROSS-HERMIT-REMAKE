
int FUN__text__0052aa54(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 *param_4
                       ,undefined4 *param_5,undefined4 *param_6)

{
  int iVar1;
  int iVar2;
  undefined4 local_c;
  undefined4 local_8;
  
  FUN__text__0053b8e6();
  FUN__text__0053ea5a();
  if (param_4 != (undefined4 *)0x0) {
    *param_4 = 0;
  }
  if (param_5 != (undefined4 *)0x0) {
    *param_5 = 0;
  }
  if (param_6 != (undefined4 *)0x0) {
    *param_6 = 0;
  }
  iVar1 = FUN__text__0053b920(param_1,param_2,0,1);
  if (-1 < iVar1) {
    iVar1 = FUN__text__00540ec8(local_c,local_8,0,1,param_3,param_4,param_5,param_6);
    iVar2 = 0;
    if (-1 < iVar1) goto LAB__text__0052aac7;
  }
  iVar2 = iVar1;
LAB__text__0052aac7:
  FUN__text__0053eb03();
  FUN__text__0053b8f3();
  return iVar2;
}

