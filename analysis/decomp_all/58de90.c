
undefined4 FUN__text__0058de90(void)

{
  int iVar1;
  int iVar2;
  int *local_8;
  
  local_8 = DAT_0080a410;
  while( true ) {
    if (*local_8 == 0) {
      return 0;
    }
    iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)(1,0,*local_8,0xffffffff,0,0,0,0);
    if (iVar1 == 0) {
      return 0xffffffff;
    }
    iVar2 = __malloc_dbg(iVar1,2,"wtombenv.c",0x3d);
    if (iVar2 == 0) {
      return 0xffffffff;
    }
    iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)(1,0,*local_8,0xffffffff,iVar2,iVar1,0,0);
    if (iVar1 == 0) break;
    FUN__text__0058e390(iVar2,0);
    local_8 = local_8 + 1;
  }
  return 0xffffffff;
}

