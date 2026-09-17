
undefined4 FUN__text__0057b7a0(void)

{
  int iVar1;
  undefined4 uVar2;
  char *local_123c;
  byte local_1238;
  char local_1230 [260];
  char local_112c [4240];
  undefined4 local_9c;
  uint local_98;
  int local_8c;
  undefined4 uStackY_24;
  char *local_8;
  
  FUN__text__0056e230();
  local_9c = 0x94;
  iVar1 = (*API_KERNEL32_DLL_GetVersionExA)();
  if (((iVar1 == 0) || (local_8c != 2)) || (local_98 < 5)) {
    iVar1 = (*DAT_00592160)();
    if (iVar1 != 0) {
      for (local_8 = local_112c; *local_8 != '\0'; local_8 = local_8 + 1) {
        if (('`' < *local_8) && (*local_8 < '{')) {
          *local_8 = *local_8 + -0x20;
        }
      }
      uStackY_24 = 0x57b863;
      iVar1 = _strncmp("__GLOBAL_HEAP_SELECTED",local_112c,0x16);
      if (iVar1 == 0) {
        local_123c = local_112c;
      }
      else {
        uStackY_24 = 0x57b88c;
        (*API_KERNEL32_DLL_GetModuleFileNameA)();
        for (local_8 = local_1230; *local_8 != '\0'; local_8 = local_8 + 1) {
          if (('`' < *local_8) && (*local_8 < '{')) {
            *local_8 = *local_8 + -0x20;
          }
        }
        local_123c = _strstr(local_112c,local_1230);
      }
      if ((local_123c != (char *)0x0) &&
         (local_8 = _strchr(local_123c,0x2c), local_8 != (char *)0x0)) {
        local_8 = local_8 + 1;
        while (*local_8 != '\0') {
          if (*local_8 == ';') {
            *local_8 = '\0';
          }
          else {
            local_8 = local_8 + 1;
          }
        }
        uStackY_24 = 0x57b968;
        iVar1 = FUN__text__00586d60();
        if (iVar1 == 2) {
          return 2;
        }
        if (iVar1 == 3) {
          return 3;
        }
        if (iVar1 == 1) {
          return 1;
        }
      }
    }
    FUN__text__0057b740();
    if (local_1238 < 6) {
      uVar2 = 2;
    }
    else {
      uVar2 = 3;
    }
  }
  else {
    uVar2 = 1;
  }
  return uVar2;
}

