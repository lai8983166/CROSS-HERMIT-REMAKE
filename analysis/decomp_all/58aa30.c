
undefined4 FUN__text__0058aa30(int param_1,undefined4 param_2,undefined4 param_3,int *param_4)

{
  byte bVar1;
  int iVar2;
  uint local_ac;
  int local_a4;
  char local_90 [128];
  char *local_10;
  size_t local_c;
  int local_8;
  
  if (param_1 != 1) {
    if (param_1 != 0) {
      return 0xffffffff;
    }
    iVar2 = FUN__text__0058d200(param_2,param_3,&DAT_0080a77c,4,0);
    if (iVar2 != 0) {
      *(char *)param_4 = '\0';
      local_a4 = 0;
      while( true ) {
        if (3 < local_a4) {
          return 0;
        }
        if (DAT_00764370 < 2) {
          bVar1 = (&DAT_0080a77c)[local_a4 * 2];
          local_ac = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 4;
        }
        else {
          bVar1 = (&DAT_0080a77c)[local_a4 * 2];
          local_ac = FUN__text__0057bb50(bVar1,4);
        }
        if (local_ac == 0) break;
        *(byte *)param_4 = (char)*param_4 * '\n' + -0x30 + bVar1;
        local_a4 = local_a4 + 1;
      }
      return 0;
    }
    return 0xffffffff;
  }
  local_10 = local_90;
  local_8 = 0;
  local_c = FUN__text__0058d3a0(param_2,param_3,local_10,0x80,0);
  if (local_c == 0) {
    iVar2 = (*API_KERNEL32_DLL_GetLastError)();
    if (((iVar2 != 0x7a) || (iVar2 = FUN__text__0058d3a0(param_2,param_3,0,0,0), iVar2 == 0)) ||
       (local_10 = (char *)__malloc_dbg(iVar2,2,"inithelp.c",0x58), local_10 == (char *)0x0))
    goto LAB__text__0058ab7d;
    local_8 = 1;
    local_c = FUN__text__0058d3a0(param_2,param_3,local_10,iVar2,0);
    if (local_c == 0) goto LAB__text__0058ab7d;
  }
  iVar2 = __malloc_dbg(local_c,2,"inithelp.c",99);
  *param_4 = iVar2;
  if (*param_4 != 0) {
    _strncpy((char *)*param_4,local_10,local_c);
    if (local_8 != 0) {
      __free_dbg(local_10,2);
    }
    return 0;
  }
LAB__text__0058ab7d:
  if (local_8 != 0) {
    __free_dbg(local_10,2);
  }
  return 0xffffffff;
}

