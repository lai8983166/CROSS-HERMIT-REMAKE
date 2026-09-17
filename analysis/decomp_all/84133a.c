
uint FUN__text1__0084133a(uint param_1,byte *param_2,uint param_3)

{
  uint uVar1;
  
  if (param_2 == (byte *)0x0) {
    param_1 = 0;
  }
  else {
    param_1 = param_1 ^ 0xffffffff;
    for (; 7 < param_3; param_3 = param_3 - 8) {
      uVar1 = *(uint *)(&DAT_00872ef4 + ((param_1 ^ *param_2) & 0xff) * 4) ^ param_1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[1]) & 0xff) * 4) ^ uVar1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[2]) & 0xff) * 4) ^ uVar1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[3]) & 0xff) * 4) ^ uVar1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[4]) & 0xff) * 4) ^ uVar1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[5]) & 0xff) * 4) ^ uVar1 >> 8;
      uVar1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[6]) & 0xff) * 4) ^ uVar1 >> 8;
      param_1 = *(uint *)(&DAT_00872ef4 + ((uVar1 ^ param_2[7]) & 0xff) * 4) ^ uVar1 >> 8;
      param_2 = param_2 + 8;
    }
    for (; param_3 != 0; param_3 = param_3 - 1) {
      param_1 = *(uint *)(&DAT_00872ef4 + ((param_1 ^ *param_2) & 0xff) * 4) ^ param_1 >> 8;
      param_2 = param_2 + 1;
    }
    param_1 = param_1 ^ 0xffffffff;
  }
  return param_1;
}

