
int FUN_0057c5e0(uint param_1,char *param_2,uint param_3)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  ulong *puVar4;
  int iVar5;
  int local_424;
  int local_41c;
  char local_418 [1028];
  int local_14;
  ulong local_10;
  char *local_c;
  char *local_8;
  
  local_14 = 0;
  local_424 = 0;
  if (param_3 == 0) {
    local_14 = 0;
  }
  else {
    iVar5 = (int)param_1 >> 5;
    if ((*(byte *)((&DAT_0080a800)[iVar5] + 4 + (param_1 & 0x1f) * 0x24) & 0x20) != 0) {
      FUN_00585ad0(param_1,0,2);
    }
    if (((int)*(char *)((&DAT_0080a800)[iVar5] + 4 + (param_1 & 0x1f) * 0x24) & 0x80U) == 0) {
      iVar2 = (*DAT_005922bc)(*(undefined4 *)((&DAT_0080a800)[iVar5] + (param_1 & 0x1f) * 0x24),
                              param_2,param_3,&local_41c,0);
      if (iVar2 == 0) {
        local_10 = (*API_KERNEL32_DLL_GetLastError)();
      }
      else {
        local_10 = 0;
        local_14 = local_41c;
      }
    }
    else {
      local_8 = param_2;
      local_10 = 0;
      do {
        if (param_3 <= (uint)((int)local_8 - (int)param_2)) break;
        local_c = local_418;
        while (((int)local_c - (int)local_418 < 0x400 &&
               ((uint)((int)local_8 - (int)param_2) < param_3))) {
          cVar1 = *local_8;
          local_8 = local_8 + 1;
          if (cVar1 == '\n') {
            local_424 = local_424 + 1;
            *local_c = '\r';
            local_c = local_c + 1;
          }
          *local_c = cVar1;
          local_c = local_c + 1;
        }
        iVar2 = (*DAT_005922bc)(*(undefined4 *)((&DAT_0080a800)[iVar5] + (param_1 & 0x1f) * 0x24),
                                local_418,(int)local_c - (int)local_418,&local_41c,0);
        if (iVar2 == 0) {
          local_10 = (*API_KERNEL32_DLL_GetLastError)();
          break;
        }
        local_14 = local_14 + local_41c;
      } while ((int)local_c - (int)local_418 <= local_41c);
    }
    if (local_14 == 0) {
      if (local_10 == 0) {
        if (((*(byte *)((&DAT_0080a800)[iVar5] + 4 + (param_1 & 0x1f) * 0x24) & 0x40) == 0) ||
           (*param_2 != '\x1a')) {
          puVar3 = (undefined4 *)FUN_00576d20();
          *puVar3 = 0x1c;
          puVar3 = (undefined4 *)FUN_00576d30();
          *puVar3 = 0;
          local_14 = -1;
        }
        else {
          local_14 = 0;
        }
      }
      else {
        if (local_10 == 5) {
          puVar3 = (undefined4 *)FUN_00576d20();
          *puVar3 = 9;
          puVar4 = (ulong *)FUN_00576d30();
          *puVar4 = local_10;
        }
        else {
          __dosmaperr(local_10);
        }
        local_14 = -1;
      }
    }
    else {
      local_14 = local_14 - local_424;
    }
  }
  return local_14;
}

