
char * FUN__text__0057d390(void)

{
  short *psVar1;
  int iVar2;
  char *pcVar3;
  int iVar4;
  char *local_1c;
  short *local_18;
  char *local_10;
  short *local_c;
  
  local_18 = (short *)0x0;
  local_1c = (char *)0x0;
  if (DAT_0080a600 == 0) {
    local_18 = (short *)(*DAT_00592110)();
    if (local_18 == (short *)0x0) {
      local_1c = (char *)(*DAT_00592114)();
      if (local_1c == (char *)0x0) {
        return (char *)0;
      }
      DAT_0080a600 = 2;
    }
    else {
      DAT_0080a600 = 1;
    }
  }
  if (DAT_0080a600 == 1) {
    if ((local_18 == (short *)0x0) &&
       (local_18 = (short *)(*DAT_00592110)(), local_18 == (short *)0x0)) {
      pcVar3 = (char *)0;
    }
    else {
      local_c = local_18;
      psVar1 = local_c;
      while (local_c = psVar1, *local_c != 0) {
        psVar1 = local_c + 1;
        if (local_c[1] == 0) {
          psVar1 = local_c + 2;
        }
      }
      iVar4 = ((int)local_c - (int)local_18 >> 1) + 1;
      iVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)(0,0,local_18,iVar4,0,0,0,0);
      if ((iVar2 == 0) ||
         (local_1c = (char *)__malloc_dbg(iVar2,2,"a_env.c",100), local_1c == (char *)0x0)) {
        (*API_KERNEL32_DLL_FreeEnvironmentStringsW)(local_18);
        pcVar3 = (char *)0;
      }
      else {
        iVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)(0,0,local_18,iVar4,local_1c,iVar2,0,0);
        if (iVar2 == 0) {
          __free_dbg(local_1c,2);
          local_1c = (char *)0x0;
        }
        (*API_KERNEL32_DLL_FreeEnvironmentStringsW)(local_18);
        pcVar3 = local_1c;
      }
    }
  }
  else if (DAT_0080a600 == 2) {
    if ((local_1c == (char *)0x0) && (local_1c = (char *)(*DAT_00592114)(), local_1c == (char *)0x0)
       ) {
      pcVar3 = (char *)0x0;
    }
    else {
      local_10 = local_1c;
      pcVar3 = local_10;
      while (local_10 = pcVar3, *local_10 != '\0') {
        pcVar3 = local_10 + 1;
        if (local_10[1] == '\0') {
          pcVar3 = local_10 + 2;
        }
      }
      pcVar3 = (char *)__malloc_dbg(local_10 + (1 - (int)local_1c),2,"a_env.c",0x8f);
      if (pcVar3 == (char *)0x0) {
        (*API_KERNEL32_DLL_FreeEnvironmentStringsA)(local_1c);
        pcVar3 = (char *)0x0;
      }
      else {
        FUN__text__0056d4d0(pcVar3,local_1c,local_10 + (1 - (int)local_1c));
        (*API_KERNEL32_DLL_FreeEnvironmentStringsA)(local_1c);
      }
    }
  }
  else {
    pcVar3 = (char *)0x0;
  }
  return pcVar3;
}

