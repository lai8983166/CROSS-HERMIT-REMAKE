
undefined4 FUN__text__005828e0(char *param_1)

{
  int iVar1;
  undefined4 uVar2;
  char local_c [8];
  
  if (((param_1 == (char *)0x0) || (*param_1 == '\0')) ||
     (iVar1 = _strcmp(param_1,(char *)&PTR_DAT_005fadb8), iVar1 == 0)) {
    iVar1 = (*DAT_0080a688)(DAT_0080a684,0x1004,local_c,8);
    if (iVar1 == 0) {
      return 0;
    }
    param_1 = local_c;
  }
  else {
    iVar1 = _strcmp(param_1,(char *)&PTR_DAT_005fadb4);
    if (iVar1 == 0) {
      iVar1 = (*DAT_0080a688)(DAT_0080a684,0xb,local_c,8);
      if (iVar1 == 0) {
        return 0;
      }
      param_1 = local_c;
    }
  }
  uVar2 = FUN__text__00572740(param_1);
  return uVar2;
}

