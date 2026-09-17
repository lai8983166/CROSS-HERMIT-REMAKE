
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00498310(void)

{
  float fVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  float10 fVar5;
  undefined4 local_84 [16];
  float local_44;
  float local_40;
  int local_3c;
  char local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  float local_24;
  float local_20;
  float local_1c;
  float local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_84;
  for (iVar2 = 0x20; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(char *)(DAT_007a49f8 + 0x24a8) != '\0') {
    local_30 = (int)*(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 4);
    local_34 = (int)*(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 6);
    local_10 = (int)((*(int *)(DAT_007a49f8 + 0x24b0) >> 0x10) +
                    (*(int *)(DAT_007a49f8 + 0x24b0) >> 0x1f & 0x1fU)) >> 5;
    local_14 = (int)((*(int *)(DAT_007a49f8 + 0x24b4) >> 0x10) +
                    (*(int *)(DAT_007a49f8 + 0x24b4) >> 0x1f & 0xfU)) >> 4;
    local_8 = (int)((int)*(short *)(DAT_007a49f8 + 0x24aa) +
                   ((int)*(short *)(DAT_007a49f8 + 0x24aa) >> 0x1f & 0x1fU)) >> 5;
    local_c = (int)((int)*(short *)(DAT_007a49f8 + 0x24ac) +
                   ((int)*(short *)(DAT_007a49f8 + 0x24ac) >> 0x1f & 0xfU)) >> 4;
    if ((local_10 == local_8) && (local_c == local_14)) {
      *(undefined1 *)(DAT_007a49f8 + 0x24a8) = 0;
      FUN__text__004977a0();
    }
    else {
      local_10 = *(int *)(DAT_007a49f8 + 0x24b0) >> 0x10;
      local_14 = *(int *)(DAT_007a49f8 + 0x24b4) >> 0x10;
      local_8 = (int)*(short *)(DAT_007a49f8 + 0x24aa);
      local_c = (int)*(short *)(DAT_007a49f8 + 0x24ac);
      local_38 = *(char *)(DAT_007a49f8 + 0x24a9);
      if (local_38 == '\0') {
        local_28 = local_8 - local_10;
        local_2c = local_c - local_14;
        local_3c = local_28 * local_28 + local_2c * local_2c;
        fVar5 = (float10)FUN__text__005711e4((double)local_3c);
        fVar1 = (float)fVar5;
        if (fVar1 <= _DAT_0059e9f4) {
          if (fVar1 <= _DAT_0059e9f0) {
            if (fVar1 <= _DAT_0059e9ec) {
              if (fVar1 <= _DAT_0059e9e8) {
                if (fVar1 <= _DAT_0059e9e4) {
                  if (fVar1 <= _DAT_0059e9e0) {
                    if (fVar1 <= _DAT_0059d910) {
                      if (fVar1 <= _DAT_0059e9dc) {
                        if (fVar1 <= _DAT_00595754) {
                          if (fVar1 <= _DAT_00595750) {
                            local_24 = 1.0;
                          }
                          else {
                            local_24 = 1.0;
                          }
                        }
                        else {
                          local_24 = 1.5;
                        }
                      }
                      else {
                        local_24 = 2.5;
                      }
                    }
                    else {
                      local_24 = 2.0;
                    }
                  }
                  else {
                    local_24 = 3.0;
                  }
                }
                else {
                  local_24 = 4.0;
                }
              }
              else {
                local_24 = 8.0;
              }
            }
            else {
              local_24 = 10.0;
            }
          }
          else {
            local_24 = 15.0;
          }
        }
        else {
          local_24 = 20.0;
        }
        fVar5 = (float10)FUN__text__005711b0((double)local_2c,(double)local_28);
        local_18 = (float)fVar5;
        fVar5 = (float10)FUN__text__0056d9d4((double)fVar5);
        local_40 = (float)fVar5;
        local_1c = (float)(fVar5 * (float10)local_24);
        fVar5 = (float10)FUN__text__0056d924((double)local_18);
        local_44 = (float)fVar5;
        local_1c = local_1c * _DAT_00592774;
        local_20 = (float)(fVar5 * (float10)local_24) * _DAT_00592774;
        iVar2 = __ftol();
        *(int *)(DAT_007a49f8 + 0x24b0) = *(int *)(DAT_007a49f8 + 0x24b0) + iVar2;
        iVar2 = __ftol();
        *(int *)(DAT_007a49f8 + 0x24b4) = *(int *)(DAT_007a49f8 + 0x24b4) + iVar2;
        iVar3 = *(int *)(DAT_007a49f8 + 0x24b0) >> 0x10;
        iVar2 = *(int *)(DAT_007a49f8 + 0x24b4) >> 0x10;
        if (iVar3 < 0) {
          *(undefined4 *)(DAT_007a49f8 + 0x24b0) = 0;
        }
        else if (local_30 * 0x20 + -0x400 <= iVar3) {
          *(int *)(DAT_007a49f8 + 0x24b0) = (local_30 * 0x20 + -0x400) * 0x10000;
        }
        if (iVar2 < 0) {
          *(undefined4 *)(DAT_007a49f8 + 0x24b4) = 0;
        }
        else if (local_34 * 0x10 + -0x238 <= iVar2) {
          *(int *)(DAT_007a49f8 + 0x24b4) = (local_34 * 0x10 + -0x238) * 0x10000;
        }
        local_10 = *(int *)(DAT_007a49f8 + 0x24b0) >> 0x10;
        local_14 = *(int *)(DAT_007a49f8 + 0x24b4) >> 0x10;
        FUN__text__0043b460(local_10,local_14);
      }
    }
  }
  local_8 = 0x498735;
  FUN__text__0056ce80();
  return;
}

