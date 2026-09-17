
int FUN_00585ad0(uint param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  ulong local_8;
  
  iVar1 = FUN_005864a0(param_1);
  if (iVar1 == -1) {
    puVar2 = (undefined4 *)FUN_00576d20();
    *puVar2 = 9;
    iVar1 = -1;
  }
  else {
    iVar1 = (*DAT_005921d8)(iVar1,param_2,0,param_3);
    if (iVar1 == -1) {
      local_8 = (*API_KERNEL32_DLL_GetLastError)();
    }
    else {
      local_8 = 0;
    }
    if (local_8 == 0) {
      *(byte *)((&DAT_0080a800)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) =
           *(byte *)((&DAT_0080a800)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 0xfd;
    }
    else {
      __dosmaperr(local_8);
      iVar1 = -1;
    }
  }
  return iVar1;
}

