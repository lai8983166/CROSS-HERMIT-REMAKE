
undefined2 FUN__text__0058b1a0(undefined2 param_1,int *param_2)

{
  undefined4 *puVar1;
  undefined *puVar2;
  uint local_1c;
  uint local_18;
  uint local_14;
  undefined *local_10;
  byte local_c;
  byte local_b;
  int local_8;
  
  if ((param_2[3] & 0x40U) == 0) {
    if (param_2[4] == -1) {
      local_10 = &DAT_007644d0;
      puVar2 = (undefined *)0x0;
    }
    else {
      puVar2 = (undefined *)((&DAT_0080a800)[param_2[4] >> 5] + (param_2[4] & 0x1fU) * 0x24);
      local_10 = puVar2;
    }
    if (((int)(char)local_10[4] & 0x80U) != 0) {
      local_8 = FUN__text__00585ca0(&local_c,CONCAT22((short)((uint)puVar2 >> 0x10),param_1));
      if (local_8 == -1) {
        puVar1 = (undefined4 *)FUN__text__00576d20();
        *puVar1 = 0x2a;
        return 0xffff;
      }
      if (local_8 == 1) {
        param_2[1] = param_2[1] + -1;
        if (param_2[1] < 0) {
          local_14 = FUN__text__005756c0((int)(char)local_c,param_2);
        }
        else {
          *(byte *)*param_2 = local_c;
          local_14 = (uint)local_c;
          *param_2 = *param_2 + 1;
        }
        if (local_14 == 0xffffffff) {
          return 0xffff;
        }
        return param_1;
      }
      param_2[1] = param_2[1] + -1;
      if (param_2[1] < 0) {
        local_18 = FUN__text__005756c0((int)(char)local_c,param_2);
      }
      else {
        *(byte *)*param_2 = local_c;
        local_18 = (uint)local_c;
        *param_2 = *param_2 + 1;
      }
      if (local_18 != 0xffffffff) {
        param_2[1] = param_2[1] + -1;
        if (param_2[1] < 0) {
          local_1c = FUN__text__005756c0((int)(char)local_b,param_2);
        }
        else {
          *(byte *)*param_2 = local_b;
          local_1c = (uint)local_b;
          *param_2 = *param_2 + 1;
        }
        if (local_1c != 0xffffffff) {
          return param_1;
        }
      }
      return 0xffff;
    }
  }
  param_2[1] = param_2[1] + -2;
  if (param_2[1] < 0) {
    param_1 = FUN__text__0058d550(param_1,param_2);
  }
  else {
    *(undefined2 *)*param_2 = param_1;
    *param_2 = *param_2 + 2;
  }
  return param_1;
}

