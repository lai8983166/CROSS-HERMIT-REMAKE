
uint FUN__text__00586800(undefined4 param_1,uint param_2,undefined4 param_3,uint param_4)

{
  undefined4 *puVar1;
  ulong uVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  uint uVar6;
  bool bVar7;
  byte local_3c;
  uint local_38;
  char local_34 [4];
  undefined4 local_30;
  uint local_2c;
  undefined4 local_28;
  undefined4 local_24;
  uint local_20;
  undefined4 local_1c;
  uint local_18;
  uint local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  local_28 = 0xc;
  local_24 = 0;
  bVar7 = (param_2 & 0x80) == 0;
  if (bVar7) {
    local_3c = 0;
  }
  else {
    local_3c = 0x10;
  }
  local_20 = (uint)bVar7;
  if ((param_2 & 0x8000) == 0) {
    if ((param_2 & 0x4000) == 0) {
      if (DAT_0080a78c != 0x8000) {
        local_3c = local_3c | 0x80;
      }
    }
    else {
      local_3c = local_3c | 0x80;
    }
  }
  uVar6 = param_2 & 3;
  if (uVar6 == 0) {
    local_38 = 0x80000000;
  }
  else if (uVar6 == 1) {
    local_38 = 0x40000000;
  }
  else {
    if (uVar6 != 2) {
      puVar1 = (undefined4 *)FUN__text__00576d20();
      *puVar1 = 0x16;
      puVar1 = (undefined4 *)FUN__text__00576d30();
      *puVar1 = 0;
      return 0xffffffff;
    }
    local_38 = 0xc0000000;
  }
  switch(param_3) {
  case 0x10:
    local_c = 0;
    break;
  default:
    puVar1 = (undefined4 *)FUN__text__00576d20();
    *puVar1 = 0x16;
    puVar1 = (undefined4 *)FUN__text__00576d30();
    *puVar1 = 0;
    return 0xffffffff;
  case 0x20:
    local_c = 1;
    break;
  case 0x30:
    local_c = 2;
    break;
  case 0x40:
    local_c = 3;
  }
  uVar6 = param_2 & 0x700;
  if (uVar6 < 0x401) {
    if (uVar6 != 0x400) {
      if (0x200 < uVar6) {
        if (uVar6 != 0x300) {
LAB__text__005869c6:
          puVar1 = (undefined4 *)FUN__text__00576d20();
          *puVar1 = 0x16;
          puVar1 = (undefined4 *)FUN__text__00576d30();
          *puVar1 = 0;
          return 0xffffffff;
        }
        local_1c = 2;
        goto LAB__text__005869e4;
      }
      if (uVar6 == 0x200) goto LAB__text__005869b4;
      if (uVar6 != 0) {
        if (uVar6 != 0x100) goto LAB__text__005869c6;
        local_1c = 4;
        goto LAB__text__005869e4;
      }
    }
    local_1c = 3;
  }
  else {
    if (uVar6 != 0x500) {
      if (uVar6 == 0x600) {
LAB__text__005869b4:
        local_1c = 5;
        goto LAB__text__005869e4;
      }
      if (uVar6 != 0x700) goto LAB__text__005869c6;
    }
    local_1c = 1;
  }
LAB__text__005869e4:
  local_2c = 0x80;
  if ((param_2 & 0x100) != 0) {
    local_14 = param_4;
    local_30 = 0;
    if ((param_4 & ~DAT_0080a3e8 & 0x80) == 0) {
      local_2c = 1;
    }
  }
  if ((param_2 & 0x40) != 0) {
    local_2c = local_2c | 0x4000000;
    local_38 = local_38 | 0x10000;
  }
  if ((param_2 & 0x1000) != 0) {
    local_2c = local_2c | 0x100;
  }
  if ((param_2 & 0x20) == 0) {
    if ((param_2 & 0x10) != 0) {
      local_2c = local_2c | 0x10000000;
    }
  }
  else {
    local_2c = local_2c | 0x8000000;
  }
  local_18 = FUN__text__00586110();
  if (local_18 == 0xffffffff) {
    puVar1 = (undefined4 *)FUN__text__00576d20();
    *puVar1 = 0x18;
    puVar1 = (undefined4 *)FUN__text__00576d30();
    *puVar1 = 0;
    local_18 = 0xffffffff;
  }
  else {
    local_8 = (*DAT_005921ec)(param_1,local_38,local_c,&local_28,local_1c,local_2c,0);
    if (local_8 == -1) {
      uVar2 = (*API_KERNEL32_DLL_GetLastError)();
      __dosmaperr(uVar2);
      FUN__text__005866b0(local_18);
      local_18 = 0xffffffff;
    }
    else {
      local_10 = (*DAT_00592104)(local_8);
      if (local_10 == 0) {
        (*DAT_00592270)(local_8);
        uVar2 = (*API_KERNEL32_DLL_GetLastError)();
        __dosmaperr(uVar2);
        FUN__text__005866b0(local_18);
        local_18 = 0xffffffff;
      }
      else {
        if (local_10 == 2) {
          local_3c = local_3c | 0x40;
        }
        else if (local_10 == 3) {
          local_3c = local_3c | 8;
        }
        __set_osfhnd(local_18,local_8);
        *(byte *)((&DAT_0080a800)[(int)local_18 >> 5] + 4 + (local_18 & 0x1f) * 0x24) = local_3c | 1
        ;
        if ((((local_3c & 0x48) == 0) && (((int)(char)(local_3c | 1) & 0x80U) != 0)) &&
           ((param_2 & 2) != 0)) {
          iVar3 = FUN__text__00585ad0(local_18,0xffffffff,2);
          if (iVar3 == -1) {
            piVar4 = (int *)FUN__text__00576d30();
            if (*piVar4 != 0x83) {
              FUN__text__00577350(local_18);
              FUN__text__005866b0(local_18);
              return 0xffffffff;
            }
          }
          else {
            local_34[0] = '\0';
            iVar5 = FUN__text__0058cad0(local_18,local_34,1);
            if (((iVar5 == 0) && (local_34[0] == '\x1a')) &&
               (iVar3 = FUN__text__0058c810(local_18,iVar3), iVar3 == -1)) {
              FUN__text__00577350(local_18);
              FUN__text__005866b0(local_18);
              return 0xffffffff;
            }
            iVar3 = FUN__text__00585ad0(local_18,0,0);
            if (iVar3 == -1) {
              FUN__text__00577350(local_18);
              FUN__text__005866b0(local_18);
              return 0xffffffff;
            }
          }
        }
        if (((local_3c & 0x48) == 0) && ((param_2 & 8) != 0)) {
          *(byte *)((&DAT_0080a800)[(int)local_18 >> 5] + 4 + (local_18 & 0x1f) * 0x24) =
               *(byte *)((&DAT_0080a800)[(int)local_18 >> 5] + 4 + (local_18 & 0x1f) * 0x24) | 0x20;
        }
        FUN__text__005866b0(local_18);
      }
    }
  }
  return local_18;
}

