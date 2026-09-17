
int FUN__text__0058cad0(uint param_1,char *param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  ulong *puVar3;
  int iVar4;
  char local_20 [4];
  int local_1c;
  char *local_18;
  int local_14;
  char *local_10;
  ulong local_c;
  char *local_8;
  
  local_1c = 0;
  local_18 = param_2;
  if ((param_3 == 0) ||
     (iVar4 = (int)param_1 >> 5,
     (*(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 2) != 0)) {
    local_1c = 0;
  }
  else {
    if (((*(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 0x48) != 0) &&
       (*(char *)((&DAT_0080a800)[iVar4] + 5 + (param_1 & 0x1f) * 0x24) != '\n')) {
      *param_2 = *(char *)((&DAT_0080a800)[iVar4] + 5 + (param_1 & 0x1f) * 0x24);
      local_18 = param_2 + 1;
      local_1c = 1;
      param_3 = param_3 + -1;
      *(undefined1 *)((&DAT_0080a800)[iVar4] + 5 + (param_1 & 0x1f) * 0x24) = 10;
    }
    iVar1 = (*DAT_005921e8)(*(undefined4 *)((&DAT_0080a800)[iVar4] + (param_1 & 0x1f) * 0x24),
                            local_18,param_3,&local_14,0);
    if (iVar1 == 0) {
      local_c = (*API_KERNEL32_DLL_GetLastError)();
      if (local_c == 5) {
        puVar2 = (undefined4 *)FUN__text__00576d20();
        *puVar2 = 9;
        puVar3 = (ulong *)FUN__text__00576d30();
        *puVar3 = local_c;
        local_1c = -1;
      }
      else if (local_c == 0x6d) {
        local_1c = 0;
      }
      else {
        __dosmaperr(local_c);
        local_1c = -1;
      }
    }
    else {
      local_1c = local_1c + local_14;
      if (((int)*(char *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 0x80U) != 0) {
        if ((local_14 == 0) || (*param_2 != '\n')) {
          *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) =
               *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 0xfb;
        }
        else {
          *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) =
               *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) | 4;
        }
        local_10 = param_2;
        local_8 = param_2;
        while (local_8 < param_2 + local_1c) {
          if (*local_8 == '\x1a') {
            if ((*(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 0x40) == 0) {
              *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) =
                   *(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) | 2;
            }
            break;
          }
          if (*local_8 == '\r') {
            if (local_8 < param_2 + local_1c + -1) {
              if (local_8[1] == '\n') {
                local_8 = local_8 + 2;
                *local_10 = '\n';
              }
              else {
                *local_10 = *local_8;
                local_8 = local_8 + 1;
              }
              local_10 = local_10 + 1;
            }
            else {
              local_8 = local_8 + 1;
              local_c = 0;
              iVar1 = (*DAT_005921e8)(*(undefined4 *)
                                       ((&DAT_0080a800)[iVar4] + (param_1 & 0x1f) * 0x24),local_20,1
                                      ,&local_14,0);
              if (iVar1 == 0) {
                local_c = (*API_KERNEL32_DLL_GetLastError)();
              }
              if ((local_c == 0) && (local_14 != 0)) {
                if ((*(byte *)((&DAT_0080a800)[iVar4] + 4 + (param_1 & 0x1f) * 0x24) & 0x48) == 0) {
                  if ((local_10 == param_2) && (local_20[0] == '\n')) {
                    *local_10 = '\n';
                    local_10 = local_10 + 1;
                  }
                  else {
                    FUN__text__00585ad0(param_1,0xffffffff,1);
                    if (local_20[0] != '\n') {
                      *local_10 = '\r';
                      local_10 = local_10 + 1;
                    }
                  }
                }
                else {
                  if (local_20[0] == '\n') {
                    *local_10 = '\n';
                  }
                  else {
                    *local_10 = '\r';
                    *(char *)((&DAT_0080a800)[iVar4] + 5 + (param_1 & 0x1f) * 0x24) = local_20[0];
                  }
                  local_10 = local_10 + 1;
                }
              }
              else {
                *local_10 = '\r';
                local_10 = local_10 + 1;
              }
            }
          }
          else {
            *local_10 = *local_8;
            local_10 = local_10 + 1;
            local_8 = local_8 + 1;
          }
        }
        local_1c = (int)local_10 - (int)param_2;
      }
    }
  }
  return local_1c;
}

