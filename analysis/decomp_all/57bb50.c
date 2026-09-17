
uint FUN_0057bb50(int param_1,uint param_2)

{
  int iVar1;
  undefined1 local_10;
  undefined1 local_f;
  undefined1 local_e;
  undefined4 local_c;
  uint local_8;
  
  if (param_1 + 1U < 0x101) {
    param_2 = *(ushort *)(PTR_DAT_00764164 + param_1 * 2) & param_2;
  }
  else {
    if ((*(ushort *)(PTR_DAT_00764164 + (param_1 >> 8 & 0xffU) * 2) & 0x8000) == 0) {
      local_10 = (undefined1)param_1;
      local_f = 0;
      local_c = 1;
    }
    else {
      local_10 = (undefined1)((uint)param_1 >> 8);
      local_f = (undefined1)param_1;
      local_e = 0;
      local_c = 2;
    }
    iVar1 = FUN_00587230(1,&local_10,local_c,&local_8,0,0,1);
    if (iVar1 == 0) {
      param_2 = 0;
    }
    else {
      param_2 = local_8 & 0xffff & param_2;
    }
  }
  return param_2;
}

