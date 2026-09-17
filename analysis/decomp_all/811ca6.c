
int FUN__text1__00811ca6(int param_1,uint param_2)

{
  int iVar1;
  
  while (0xff < param_2) {
    iVar1 = DAT_00874448 + param_2 * 0xc;
    *(undefined1 *)(DAT_00874428 + param_1) = *(undefined1 *)(iVar1 + 8);
    param_1 = param_1 + 1;
    param_2 = *(uint *)(iVar1 + 4);
  }
  *(undefined1 *)(DAT_00874428 + param_1) = (undefined1)param_2;
  return param_1 + 1;
}

