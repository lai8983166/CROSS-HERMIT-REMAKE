
int FUN__text__0052a871(undefined4 param_1,undefined4 param_2,undefined4 *param_3,
                       undefined4 *param_4,undefined4 *param_5)

{
  int iVar1;
  int iVar2;
  undefined4 local_c;
  undefined4 local_8;
  
  FUN__text__0053b6ae();
  FUN__text__0053ea5a();
  if (param_3 != (undefined4 *)0x0) {
    *param_3 = 0;
  }
  if (param_4 != (undefined4 *)0x0) {
    *param_4 = 0;
  }
  if (param_5 != (undefined4 *)0x0) {
    *param_5 = 0;
  }
  iVar1 = FUN__text__0053b6c0(param_1,0);
  if (-1 < iVar1) {
    iVar1 = FUN__text__00540ec8(local_c,local_8,param_1,1,param_2,param_3,param_4,param_5);
    iVar2 = 0;
    if (-1 < iVar1) goto LAB__text__0052a8e1;
  }
  iVar2 = iVar1;
LAB__text__0052a8e1:
  FUN__text__0053eb03();
  FUN__text__0053b8db();
  return iVar2;
}

