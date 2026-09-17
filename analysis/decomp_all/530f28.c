
int __thiscall FUN__text__00530f28(int *param_1,int param_2,undefined4 param_3,uint param_4)

{
  int iVar1;
  
  param_1[1] = 0;
  *param_1 = 0;
  param_1[2] = param_4;
  if ((((param_4 & 0xffff) == 0) || (5 < (param_4 & 0xffff))) || ((param_4 & 0xfff00000) != 0)) {
    return -0x7789f794;
  }
  *(uint *)(param_2 + 0x40) = param_4 & 0x80000;
  iVar1 = FUN__text__005369c1(param_2);
  param_1[1] = iVar1;
  if (iVar1 != 0) {
    iVar1 = FUN__text__005369c1(param_3);
    *param_1 = iVar1;
    if (iVar1 != 0) {
      iVar1 = FUN__text__00532365(iVar1);
      if (iVar1 < 0) goto LAB__text__00531014;
      iVar1 = FUN__text__0052f08b();
      if ((((-1 < iVar1) || (iVar1 = FUN__text__0052f1c3(), -1 < iVar1)) ||
          ((iVar1 = FUN__text__0052f2b4(), -1 < iVar1 ||
           ((iVar1 = FUN__text__0052f4b6(), -1 < iVar1 ||
            (iVar1 = FUN__text__0052f6ba(), -1 < iVar1)))))) ||
         ((iVar1 = FUN__text__0052fadd(), -1 < iVar1 ||
          ((((iVar1 = FUN__text__0053006f(), -1 < iVar1 ||
             (iVar1 = FUN__text__00530455(), -1 < iVar1)) ||
            (iVar1 = FUN__text__00530b86(), -1 < iVar1)) ||
           (iVar1 = FUN__text__0052d9e8(), -1 < iVar1)))))) {
        iVar1 = 0;
        goto LAB__text__00531014;
      }
    }
  }
  iVar1 = -0x7fffbffb;
LAB__text__00531014:
  if ((undefined4 *)param_1[1] != (undefined4 *)0x0) {
    (*(code *)**(undefined4 **)param_1[1])(1);
    param_1[1] = 0;
  }
  if ((undefined4 *)*param_1 != (undefined4 *)0x0) {
    (*(code *)**(undefined4 **)*param_1)(1);
    *param_1 = 0;
  }
  return iVar1;
}

