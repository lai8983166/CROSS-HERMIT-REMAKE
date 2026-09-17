
undefined4 * FUN_005753b0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *local_8;
  
  uVar1 = (*API_KERNEL32_DLL_GetLastError)();
  local_8 = (undefined4 *)(*API_KERNEL32_DLL_TlsGetValue)(DAT_00761bc0,uVar1);
  if (local_8 == (undefined4 *)0x0) {
    local_8 = (undefined4 *)__calloc_dbg(1,0x74,2,"tidtable.c",0xe7);
    if (local_8 != (undefined4 *)0x0) {
      iVar2 = (*API_KERNEL32_DLL_TlsSetValue)(DAT_00761bc0,local_8);
      if (iVar2 != 0) {
        FUN_00575390(local_8);
        uVar3 = (*API_KERNEL32_DLL_GetCurrentThreadId)();
        *local_8 = uVar3;
        local_8[1] = 0xffffffff;
        goto LAB_00575437;
      }
    }
    __amsg_exit(0x10);
  }
LAB_00575437:
  (*API_KERNEL32_DLL_SetLastError)(uVar1);
  return local_8;
}

