
/* WARNING: Removing unreachable block (ram,0x00471495) */
/* WARNING: Removing unreachable block (ram,0x004714b8) */

void __thiscall FUN__text__00471070(int param_1,int param_2,undefined4 param_3,int param_4)

{
  short sVar1;
  short sVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_88 [16];
  char local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_88;
  for (iVar4 = 0x21; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_10 = (int)((*(int *)(param_2 + 0x2ec) >> 0x10) + (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)
                  ) >> 5;
  local_14 = (int)((*(int *)(param_2 + 0x2f0) >> 0x10) + (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU))
             >> 4;
  local_18 = (int)((int)*(short *)(param_2 + 0x4d0) +
                  ((int)*(short *)(param_2 + 0x4d0) >> 0x1f & 0x1fU)) >> 5;
  local_1c = (int)((int)*(short *)(param_2 + 0x4d2) +
                  ((int)*(short *)(param_2 + 0x4d2) >> 0x1f & 0xfU)) >> 4;
  local_20 = local_18 - local_10;
  local_24 = local_1c - local_14;
  if (local_20 < 0) {
    local_3c = -1;
    local_20 = -local_20;
  }
  else {
    local_3c = 1;
  }
  if (local_24 < 0) {
    local_40 = -1;
    local_24 = -local_24;
  }
  else {
    local_40 = 1;
  }
  local_30 = 0;
  local_2c = 0;
  local_38 = 0;
  local_34 = 0;
  local_28 = 0;
  iVar4 = param_4 + -1;
  local_8 = param_1;
  if (local_20 < local_24) {
    for (local_c = 0; local_c < local_24; local_c = local_c + 1) {
      local_30 = local_30 + local_40;
      local_28 = local_28 + local_20;
      if (local_24 <= local_28) {
        local_2c = local_2c + local_3c;
        local_28 = local_28 - local_24;
      }
      local_44 = (local_30 + 0xf) * 0x1f + 0xf + local_2c;
      if ((*(char *)(local_8 + local_44 + 0x108f7c) != -1) &&
         (*(char *)(local_8 + local_44 + 0x108f7c) != '\0')) {
        local_34 = local_2c;
        local_38 = local_30;
      }
      iVar3 = FUN__text__0056db00(local_2c);
      if ((iVar4 <= iVar3) || (iVar3 = FUN__text__0056db00(local_30), iVar4 <= iVar3)) break;
    }
  }
  else {
    for (local_c = 0; local_c < local_20; local_c = local_c + 1) {
      local_2c = local_2c + local_3c;
      local_28 = local_28 + local_24;
      if (local_20 <= local_28) {
        local_30 = local_30 + local_40;
        local_28 = local_28 - local_20;
      }
      local_44 = (local_30 + 0xf) * 0x1f + 0xf + local_2c;
      if ((*(char *)(local_8 + local_44 + 0x108f7c) != -1) &&
         (*(char *)(local_8 + local_44 + 0x108f7c) != '\0')) {
        local_38 = local_30;
        local_34 = local_2c;
      }
      iVar3 = FUN__text__0056db00(local_2c);
      if ((iVar4 <= iVar3) || (iVar3 = FUN__text__0056db00(local_30), iVar4 <= iVar3)) break;
    }
  }
  local_2c = local_34;
  local_30 = local_38;
  local_44 = (local_38 + 0xf) * 0x1f + 0xf + local_34;
  local_48 = *(char *)(local_8 + local_44 + 0x108f7c);
  if (local_48 == -1) {
    *(short *)(param_2 + 0x4dc) = (short)(local_10 << 5) + 0x10;
    *(short *)(param_2 + 0x4de) = (short)(local_14 << 4) + 8;
    *(short *)(param_2 + 0x4dc) = (short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    *(short *)(param_2 + 0x4de) = (short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
  }
  else if (local_48 == '\0') {
    *(short *)(param_2 + 0x4dc) = ((short)local_10 + (short)local_34) * 0x20 + 0x10;
    *(short *)(param_2 + 0x4de) = ((short)local_14 + (short)local_38) * 0x10 + 8;
  }
  else if ((local_34 == 0) && (local_38 == 0)) {
    if ((local_20 == 0) && (local_24 == 0)) {
      *(short *)(param_2 + 0x4dc) = (short)(local_10 << 5) + 0x10;
      *(short *)(param_2 + 0x4de) = (short)(local_14 << 4) + 8;
      *(undefined2 *)(param_2 + 0x4dc) = *(undefined2 *)(param_2 + 0x4d0);
      *(undefined2 *)(param_2 + 0x4de) = *(undefined2 *)(param_2 + 0x4d2);
    }
    else {
      *(short *)(param_2 + 0x4dc) = (short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
      *(short *)(param_2 + 0x4de) = (short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    }
  }
  else {
    while( true ) {
      local_38 = local_30;
      iVar3 = FUN__text__0056db00(local_2c);
      if (iVar3 < 0x10) {
        FUN__text__0056db00(local_30);
      }
      local_44 = (local_30 + 0xf) * 0x1f + 0xf + local_2c;
      if (((((int)*(char *)(local_8 + local_44 + 0x108f7c) == param_4 + -2) && (local_2c != 0)) &&
          (local_30 != 0)) || (*(char *)(local_8 + local_44 + 0x108f7c) == iVar4)) break;
      local_34 = local_2c + 1;
      local_44 = (local_30 + 0xe) * 0x1f + 0xf + local_34;
      if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
        local_2c = local_2c + 1;
        local_48 = *(char *)((local_30 + 0xe) * 0x1f + local_8 + 0x108f8b + local_34);
        local_30 = local_30 + -1;
      }
      else {
        local_34 = local_2c + -1;
        local_44 = (local_30 + 0xe) * 0x1f + 0xf + local_34;
        if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
          local_2c = local_2c + -1;
          local_48 = *(char *)((local_30 + 0xe) * 0x1f + local_8 + 0x108f8b + local_34);
          local_30 = local_30 + -1;
        }
        else {
          local_34 = local_2c + -1;
          local_44 = (local_30 + 0x10) * 0x1f + 0xf + local_34;
          if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
            local_2c = local_2c + -1;
            local_48 = *(char *)((local_30 + 0x10) * 0x1f + local_8 + 0x108f8b + local_34);
            local_30 = local_30 + 1;
          }
          else {
            local_34 = local_2c + 1;
            local_44 = (local_30 + 0x10) * 0x1f + 0xf + local_34;
            if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
              local_2c = local_2c + 1;
              local_48 = *(char *)((local_30 + 0x10) * 0x1f + local_8 + 0x108f8b + local_34);
              local_30 = local_30 + 1;
            }
            else {
              local_34 = local_2c;
              local_44 = (local_30 + 0xe) * 0x1f + 0xf + local_2c;
              if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
                local_48 = *(char *)((local_30 + 0xe) * 0x1f + local_8 + 0x108f8b + local_2c);
                local_30 = local_30 + -1;
              }
              else {
                local_44 = (local_30 + 0x10) * 0x1f + 0xf + local_2c;
                if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
                  local_48 = *(char *)((local_30 + 0x10) * 0x1f + local_8 + 0x108f8b + local_2c);
                  local_30 = local_30 + 1;
                }
                else {
                  local_34 = local_2c + 1;
                  local_44 = (local_30 + 0xf) * 0x1f + 0xf + local_34;
                  if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
                    local_2c = local_2c + 1;
                    local_48 = *(char *)((local_30 + 0xf) * 0x1f + local_8 + 0x108f8b + local_34);
                  }
                  else {
                    local_34 = local_2c + -1;
                    local_44 = (local_30 + 0xf) * 0x1f + 0xf + local_34;
                    if (local_48 < *(char *)(local_8 + local_44 + 0x108f7c)) {
                      local_2c = local_2c + -1;
                      local_48 = *(char *)((local_30 + 0xf) * 0x1f + local_8 + 0x108f8b + local_34);
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    sVar1 = (short)local_10;
    sVar2 = (short)local_14;
    if ((local_2c == 0) && (local_30 == -1)) {
      *(short *)(param_2 + 0x4dc) = sVar1 * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + -1) * 0x10 + 8;
    }
    else if ((local_2c == 0) && (local_30 == 1)) {
      *(short *)(param_2 + 0x4dc) = sVar1 * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + 1) * 0x10 + 8;
    }
    else if ((local_2c == 1) && (local_30 == 0)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + 1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = sVar2 * 0x10 + 8;
    }
    else if ((local_2c == -1) && (local_30 == 0)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + -1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = sVar2 * 0x10 + 8;
    }
    else if ((local_2c == 1) && (local_30 == -1)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + 1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + -1) * 0x10 + 8;
    }
    else if ((local_2c == -1) && (local_30 == -1)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + -1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + -1) * 0x10 + 8;
    }
    else if ((local_2c == 1) && (local_30 == 1)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + 1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + 1) * 0x10 + 8;
    }
    else if ((local_2c == -1) && (local_30 == 1)) {
      *(short *)(param_2 + 0x4dc) = (sVar1 + -1) * 0x20 + 0x10;
      *(short *)(param_2 + 0x4de) = (sVar2 + 1) * 0x10 + 8;
    }
  }
  local_8 = 0x471aaa;
  FUN__text__0056ce80();
  return;
}

