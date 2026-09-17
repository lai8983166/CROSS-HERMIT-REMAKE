
void __thiscall FUN__text__0042b360(int *param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  uint local_14;
  undefined4 local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 == 0) {
    local_8 = param_1;
    (*API_KERNEL32_DLL_lstrlenA)(param_3);
    local_14 = FUN__text__0056ce80();
    if (local_14 < 0x40) {
      (*API_USER32_DLL_GetWindowLongA)(param_2,0xfffffffa);
      local_10 = FUN__text__0056ce80();
      (*API_USER32_DLL_LoadIconA)(local_10,(short)local_8[0x17]);
      local_c = FUN__text__0056ce80();
      local_8[1] = 0x58;
      local_8[4] = 7;
      local_8[2] = param_2;
      local_8[6] = local_c;
      local_8[5] = 0x414;
      local_8[3] = 0x65;
      FUN__text__0056cd90(local_8 + 7,param_3);
      (*API_SHELL32_DLL_Shell_NotifyIconA)(0,local_8 + 1);
      FUN__text__0056ce80();
      *local_8 = 1;
    }
  }
  local_8 = (int *)0x42b46b;
  FUN__text__0056ce80();
  return;
}

