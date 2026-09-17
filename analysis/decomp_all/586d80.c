
uint FUN__text__00586d80(byte *param_1,undefined4 *param_2,uint param_3,uint param_4)

{
  byte bVar1;
  byte *pbVar2;
  uint uVar3;
  int iVar4;
  undefined4 *puVar5;
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  uint local_10;
  byte *local_8;
  
  local_10 = 0;
  bVar1 = *param_1;
  pbVar2 = param_1;
  while( true ) {
    local_8 = pbVar2 + 1;
    if (DAT_00764370 < 2) {
      local_1c = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 8;
    }
    else {
      local_1c = FUN__text__0057bb50(bVar1,8);
    }
    if (local_1c == 0) break;
    bVar1 = *local_8;
    pbVar2 = local_8;
  }
  if (bVar1 == 0x2d) {
    param_4 = param_4 | 2;
    bVar1 = *local_8;
    local_8 = pbVar2 + 2;
  }
  else if (bVar1 == 0x2b) {
    bVar1 = *local_8;
    local_8 = pbVar2 + 2;
  }
  if ((((int)param_3 < 0) || (param_3 == 1)) || (0x24 < (int)param_3)) {
    if (param_2 != (undefined4 *)0x0) {
      *param_2 = param_1;
    }
    return 0;
  }
  if (param_3 == 0) {
    if (bVar1 == 0x30) {
      if ((*local_8 == 0x78) || (*local_8 == 0x58)) {
        param_3 = 0x10;
      }
      else {
        param_3 = 8;
      }
    }
    else {
      param_3 = 10;
    }
  }
  if (((param_3 == 0x10) && (bVar1 == 0x30)) && ((*local_8 == 0x78 || (*local_8 == 0x58)))) {
    bVar1 = local_8[1];
    local_8 = local_8 + 2;
  }
  uVar3 = (uint)(0xffffffff / (ulonglong)param_3);
  do {
    if (DAT_00764370 < 2) {
      local_20 = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 4;
    }
    else {
      local_20 = FUN__text__0057bb50(bVar1,4);
    }
    if (local_20 == 0) {
      if (DAT_00764370 < 2) {
        local_24 = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 0x103;
      }
      else {
        local_24 = FUN__text__0057bb50(bVar1,0x103);
      }
      if (local_24 == 0) {
LAB__text__00586ff0:
        local_8 = local_8 + -1;
        if ((param_4 & 8) == 0) {
          if (param_2 != (undefined4 *)0x0) {
            local_8 = param_1;
          }
          local_10 = 0;
        }
        else if (((param_4 & 4) != 0) ||
                (((param_4 & 1) == 0 &&
                 ((((param_4 & 2) != 0 && (0x80000000 < local_10)) ||
                  (((param_4 & 2) == 0 && (0x7fffffff < local_10)))))))) {
          puVar5 = (undefined4 *)FUN__text__00576d20();
          *puVar5 = 0x22;
          if ((param_4 & 1) == 0) {
            if ((param_4 & 2) == 0) {
              local_10 = 0x7fffffff;
            }
            else {
              local_10 = 0x80000000;
            }
          }
          else {
            local_10 = 0xffffffff;
          }
        }
        if (param_2 != (undefined4 *)0x0) {
          *param_2 = local_8;
        }
        if ((param_4 & 2) == 0) {
          return local_10;
        }
        return -local_10;
      }
      iVar4 = FUN__text__0058cf30((int)(char)bVar1);
      local_18 = iVar4 - 0x37;
    }
    else {
      local_18 = (int)(char)bVar1 - 0x30;
    }
    if (param_3 <= local_18) goto LAB__text__00586ff0;
    if ((local_10 < uVar3) ||
       ((local_10 == uVar3 && (local_18 <= (uint)(0xffffffff % (ulonglong)param_3))))) {
      local_10 = local_10 * param_3 + local_18;
      param_4 = param_4 | 8;
    }
    else {
      param_4 = param_4 | 0xc;
    }
    bVar1 = *local_8;
    local_8 = local_8 + 1;
  } while( true );
}

