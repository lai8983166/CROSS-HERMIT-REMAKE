
undefined4 FUN__text__00581f90(char *param_1,undefined2 *param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  uint _Value;
  code *local_c;
  undefined2 local_8;
  
  if (DAT_0080a688 == (code *)0x0) {
    iVar1 = FUN__text__00582a60();
    if (iVar1 == 0) {
      local_c = crtGetLocaleInfoA;
    }
    else {
      local_c = API_KERNEL32_DLL_GetLocaleInfoA;
    }
    DAT_0080a688 = local_c;
  }
  if (param_1 == (char *)0x0) {
    FUN__text__005828b0();
  }
  else {
    DAT_0080a678 = param_1;
    if ((param_1 != (char *)0x0) && (*param_1 != '\0')) {
      FUN__text__00582190(&PTR_s_american_00764c90,0x40,&DAT_0080a678);
    }
    DAT_0080a67c = param_1 + 0x40;
    if ((DAT_0080a67c != (char *)0x0) && (*DAT_0080a67c != '\0')) {
      FUN__text__00582190(&PTR_s_america_00764bd8,0x16,&DAT_0080a67c);
    }
    DAT_0080a680 = 0;
    if ((DAT_0080a678 == (char *)0x0) || (*DAT_0080a678 == '\0')) {
      if ((DAT_0080a67c == (char *)0x0) || (*DAT_0080a67c == '\0')) {
        FUN__text__005828b0();
      }
      else {
        FUN__text__005827b0();
      }
    }
    else if ((DAT_0080a67c == (char *)0x0) || (*DAT_0080a67c == '\0')) {
      FUN__text__00582610();
    }
    else {
      FUN__text__00582220();
    }
  }
  if (DAT_0080a680 == 0) {
    uVar2 = 0;
  }
  else {
    _Value = FUN__text__005828e0(param_1 + 0x80);
    if ((_Value == 0) || (iVar1 = (*API_KERNEL32_DLL_IsValidCodePage)(_Value & 0xffff), iVar1 == 0))
    {
      uVar2 = 0;
    }
    else {
      iVar1 = (*API_KERNEL32_DLL_IsValidLocale)(DAT_0080a668,1);
      if (iVar1 == 0) {
        uVar2 = 0;
      }
      else {
        if (param_2 != (undefined2 *)0x0) {
          *param_2 = (undefined2)DAT_0080a668;
          param_2[1] = (undefined2)DAT_0080a684;
          local_8 = (undefined2)_Value;
          param_2[2] = local_8;
        }
        if (param_3 != 0) {
          iVar1 = (*DAT_0080a688)(DAT_0080a668,0x1001,param_3,0x40);
          if (iVar1 == 0) {
            return 0;
          }
          iVar1 = (*DAT_0080a688)(DAT_0080a684,0x1002,param_3 + 0x40,0x40);
          if (iVar1 == 0) {
            return 0;
          }
          __itoa(_Value,(char *)(param_3 + 0x80),10);
        }
        uVar2 = 1;
      }
    }
  }
  return uVar2;
}

