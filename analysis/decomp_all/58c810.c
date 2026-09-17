
int FUN__text__0058c810(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  int *piVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  int local_1020;
  int local_101c;
  undefined1 local_1008 [4064];
  undefined4 uStackY_28;
  undefined4 uStackY_24;
  char *pcStackY_20;
  
  FUN__text__0056e230();
  local_1020 = 0;
  if (param_2 < 0) {
    pcStackY_20 = "chsize.c";
    uStackY_24 = 2;
    uStackY_28 = 0x58c854;
    iVar2 = FUN__text__00573780();
    if (iVar2 == 1) {
      pcVar1 = (code *)swi(3);
      iVar2 = (*pcVar1)();
      return iVar2;
    }
  }
  pcStackY_20 = (char *)0x58c870;
  iVar2 = FUN__text__00585ad0();
  if (iVar2 != -1) {
    pcStackY_20 = (char *)0x58c88f;
    local_101c = FUN__text__00585ad0();
    if (local_101c != -1) {
      local_101c = param_2 - local_101c;
      if (local_101c < 1) {
        if (local_101c < 0) {
          pcStackY_20 = (char *)0x58c9d8;
          FUN__text__00585ad0();
          FUN__text__005864a0();
          iVar2 = (*API_KERNEL32_DLL_SetEndOfFile)();
          local_1020 = (iVar2 != 0) - 1;
          if (local_1020 == -1) {
            puVar4 = (undefined4 *)FUN__text__00576d20();
            *puVar4 = 0xd;
            uVar5 = (*API_KERNEL32_DLL_GetLastError)();
            puVar4 = (undefined4 *)FUN__text__00576d30();
            *puVar4 = uVar5;
          }
        }
      }
      else {
        pcStackY_20 = (char *)0x58c8d8;
        _memset(local_1008,0,0x1000);
        FUN__text__0058dd70();
        do {
          pcStackY_20 = (char *)0x58c95a;
          iVar2 = FUN__text__0057c5e0();
          if (iVar2 == -1) {
            piVar3 = (int *)FUN__text__00576d30();
            if (*piVar3 == 5) {
              puVar4 = (undefined4 *)FUN__text__00576d20();
              *puVar4 = 0xd;
            }
            local_1020 = -1;
            break;
          }
          local_101c = local_101c - iVar2;
        } while (0 < local_101c);
        FUN__text__0058dd70();
      }
      pcStackY_20 = (char *)0x58ca30;
      FUN__text__00585ad0();
      return local_1020;
    }
  }
  return -1;
}

