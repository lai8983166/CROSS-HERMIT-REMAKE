
uint FUN__text__0058cfd0(uint param_1)

{
  int iVar1;
  uint local_14;
  uint local_10;
  undefined1 local_c;
  undefined1 local_b;
  undefined1 local_a;
  undefined4 local_8;
  
  if (DAT_0080a62c == 0) {
    if ((0x60 < (int)param_1) && ((int)param_1 < 0x7b)) {
      param_1 = param_1 - 0x20;
    }
  }
  else {
    if ((int)param_1 < 0x100) {
      if (DAT_00764370 < 2) {
        local_14 = *(ushort *)(PTR_DAT_00764164 + param_1 * 2) & 2;
      }
      else {
        local_14 = FUN__text__0057bb50(param_1,2);
      }
      if (local_14 == 0) {
        return param_1;
      }
    }
    if ((*(ushort *)(PTR_DAT_00764164 + ((int)param_1 >> 8 & 0xffU) * 2) & 0x8000) == 0) {
      local_c = (undefined1)param_1;
      local_b = 0;
      local_8 = 1;
    }
    else {
      local_c = (undefined1)(param_1 >> 8);
      local_b = (undefined1)param_1;
      local_a = 0;
      local_8 = 2;
    }
    iVar1 = FUN__text__005873f0(DAT_0080a62c,0x200,&local_c,local_8,&local_10,3,0,1);
    if (iVar1 != 0) {
      if (iVar1 == 1) {
        param_1 = local_10 & 0xff;
      }
      else {
        param_1 = local_10 & 0xff | (local_10 >> 8 & 0xff) << 8;
      }
    }
  }
  return param_1;
}

