
undefined4 __fastcall FUN__text__005752d0(undefined4 param_1)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 uVar3;
  
  FUN__text__00576f60(param_1);
  DAT_00761bc0 = (*API_KERNEL32_DLL_TlsAlloc)();
  if (((DAT_00761bc0 != -1) &&
      (puVar1 = (undefined4 *)__calloc_dbg(1,0x74,2,"tidtable.c",0x61), puVar1 != (undefined4 *)0x0)
      ) && (iVar2 = (*API_KERNEL32_DLL_TlsSetValue)(DAT_00761bc0,puVar1), iVar2 != 0)) {
    FUN__text__00575390(puVar1);
    uVar3 = (*API_KERNEL32_DLL_GetCurrentThreadId)();
    *puVar1 = uVar3;
    puVar1[1] = 0xffffffff;
    return 1;
  }
  return 0;
}

