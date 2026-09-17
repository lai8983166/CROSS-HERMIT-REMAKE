
bool FUN__text1__0080fac0(undefined4 param_1,undefined4 param_2,uint *param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  int local_1c;
  undefined1 local_18;
  int local_10;
  undefined1 local_8;
  char local_7;
  
  DAT_00874420 = '\0';
  FUN__text1__008105b0(param_2,param_4,1);
  FUN__text1__0080fb61(param_1,*param_3,&local_1c);
  iVar1 = FUN__text1__00810624(local_18);
  iVar2 = FUN__text1__00810624(local_8);
  *param_3 = ((iVar1 + (local_10 - (local_1c + 1)) * 8) - iVar2) + 0xfU >> 3;
  if (local_7 != '\0') {
    DAT_00874420 = '\x01';
  }
  return DAT_00874420 == '\0';
}

