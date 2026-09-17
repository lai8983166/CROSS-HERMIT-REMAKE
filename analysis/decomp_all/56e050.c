
int FUN__text__0056e050(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                       undefined4 param_5,undefined4 param_6)

{
  int iVar1;
  int iVar2;
  ulong local_10;
  
  local_10 = 0;
  iVar1 = __calloc_dbg(1,0x74,2,"threadex.c",0x6c);
  if (iVar1 != 0) {
    FUN__text__00575390(iVar1);
    *(undefined4 *)(iVar1 + 0x48) = param_3;
    *(undefined4 *)(iVar1 + 0x4c) = param_4;
    *(undefined4 *)(iVar1 + 4) = 0xffffffff;
    iVar2 = (*DAT_0059221c)(param_1,param_2,FUN__text__0056e110,iVar1,param_5,param_6);
    if (iVar2 != 0) {
      return iVar2;
    }
    local_10 = (*API_KERNEL32_DLL_GetLastError)();
  }
  __free_dbg(iVar1,2);
  if (local_10 != 0) {
    __dosmaperr(local_10);
  }
  return 0;
}

