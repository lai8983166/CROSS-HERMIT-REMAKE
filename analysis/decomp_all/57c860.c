
int FUN__text__0057c860(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6,
                       int param_7)

{
  uint uVar1;
  int iVar2;
  int local_30;
  undefined1 local_2c [8];
  int local_24;
  int local_1c;
  uint local_18;
  int local_10;
  int local_8;
  
  uVar1 = param_1 - 0x76c;
  if (((int)uVar1 < 0x46) || (0x8a < (int)uVar1)) {
    local_8 = -1;
  }
  else {
    local_30 = param_3 + *(int *)(&DAT_00764fb4 + param_2 * 4);
    if (((uVar1 & 3) == 0) && (2 < param_2)) {
      local_30 = local_30 + 1;
    }
    local_8 = ((((param_1 + -0x76d >> 2) + -0x11 + local_30 + (param_1 + -0x7b2) * 0x16d) * 0x18 +
               param_4) * 0x3c + param_5) * 0x3c + param_6;
    FUN__text__00587750();
    local_8 = local_8 + DAT_00764ed0;
    local_10 = local_30;
    local_1c = param_2 + -1;
    local_24 = param_4;
    if ((param_7 == 1) ||
       (((param_7 == -1 && (DAT_00764ed4 != 0)) &&
        (local_18 = uVar1, iVar2 = FUN__text__00587b60(local_2c), iVar2 != 0)))) {
      local_8 = local_8 + DAT_00764ed8;
    }
  }
  return local_8;
}

