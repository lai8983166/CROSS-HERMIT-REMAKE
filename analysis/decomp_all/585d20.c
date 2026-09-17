
int FUN_00585d20(undefined1 *param_1,uint param_2)

{
  undefined4 *puVar1;
  int local_c;
  int local_8;
  
  if (param_1 == (undefined1 *)0x0) {
    local_8 = 0;
  }
  else if (DAT_0080a62c == 0) {
    if ((param_2 & 0xffff) < 0x100) {
      *param_1 = (undefined1)param_2;
      local_8 = 1;
    }
    else {
      puVar1 = (undefined4 *)FUN_00576d20();
      *puVar1 = 0x2a;
      local_8 = -1;
    }
  }
  else {
    local_c = 0;
    local_8 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                        (DAT_0080a63c,0x220,&param_2,1,param_1,DAT_00764370,0,&local_c);
    if ((local_8 == 0) || (local_c != 0)) {
      puVar1 = (undefined4 *)FUN_00576d20();
      *puVar1 = 0x2a;
      local_8 = -1;
    }
  }
  return local_8;
}

