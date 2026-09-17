
undefined4 FUN__text1__0084cc2e(byte param_1,uint param_2,byte param_3)

{
  if ((*(byte *)((int)&DAT_00875a00 + param_1 + 1) & param_3) == 0) {
    if (param_2 == 0) {
      param_2 = 0;
    }
    else {
      param_2 = *(ushort *)(&DAT_0087026a + (uint)param_1 * 2) & param_2;
    }
    if (param_2 == 0) {
      return 0;
    }
  }
  return 1;
}

