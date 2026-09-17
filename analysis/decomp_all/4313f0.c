
void FUN__text__004313f0(void *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  short *local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_1,0,0x382);
  local_14 = 0;
  do {
    if (local_14 == 0xfa) {
      for (local_14 = 0; local_14 != 0x10; local_14 = local_14 + 1) {
        *(undefined2 *)((int)param_1 + local_14 * 2 + 0x360) = 0;
      }
      for (local_14 = 0; local_14 != 4; local_14 = local_14 + 1) {
        local_18 = FUN__text__00431a60(local_14);
        *(short *)((int)param_1 + local_18 * 2 + 0x360) =
             *(short *)((int)param_1 + local_18 * 2 + 0x360) +
             *(short *)((int)param_1 + local_14 * 0x32 + 0x1e);
      }
      local_8 = 0x431883;
      FUN__text__0056ce80();
      return;
    }
    local_10 = local_8 + 0x80aec + local_14 * 0x520;
    iVar1 = FUN__text__00468d10(local_10);
    if (iVar1 != 0) {
      local_c = (short *)((int)param_1 + (uint)*(byte *)(*(int *)(local_10 + 600) + 0xa4) * 0x32);
      iVar1 = FUN__text__00468e10(local_10);
      if (iVar1 == 0) {
        iVar1 = FUN__text__00469ad0(local_10);
        if (iVar1 == 0) {
LAB__text__004315e2:
          iVar1 = FUN__text__00469c60(local_10);
          if (iVar1 == 0) {
            iVar1 = FUN__text__00469b90(local_10);
            if (iVar1 == 0) {
              iVar1 = FUN__text__00469480(local_10);
              if (iVar1 == 0) {
                iVar1 = FUN__text__00469220(local_10);
                if (iVar1 == 0) {
                  local_c[0x14] = local_c[0x14] + 1;
                }
                else {
                  local_c[0x13] = local_c[0x13] + 1;
                }
              }
              else {
                local_c[0x12] = local_c[0x12] + 1;
              }
            }
            else {
              iVar1 = FUN__text__00469480(local_10);
              if (iVar1 == 0) {
                iVar1 = FUN__text__00469220(local_10);
                if (iVar1 == 0) {
                  local_c[0x17] = local_c[0x17] + 1;
                }
                else {
                  local_c[0x16] = local_c[0x16] + 1;
                }
              }
              else {
                local_c[0x15] = local_c[0x15] + 1;
              }
            }
          }
          else {
            iVar1 = FUN__text__00469d30(local_10);
            if (iVar1 != 0) {
              iVar1 = FUN__text__00469480(local_10);
              if (iVar1 == 0) {
                iVar1 = FUN__text__00469220(local_10);
                if (iVar1 == 0) {
                  local_c[0xb] = local_c[0xb] + 1;
                }
                else {
                  local_c[10] = local_c[10] + 1;
                }
              }
              else {
                local_c[9] = local_c[9] + 1;
              }
            }
            iVar1 = FUN__text__00469df0(local_10);
            if (iVar1 != 0) {
              iVar1 = FUN__text__00469480(local_10);
              if (iVar1 == 0) {
                iVar1 = FUN__text__00469220(local_10);
                if (iVar1 == 0) {
                  local_c[0xe] = local_c[0xe] + 1;
                }
                else {
                  local_c[0xd] = local_c[0xd] + 1;
                }
              }
              else {
                local_c[0xc] = local_c[0xc] + 1;
              }
            }
            iVar1 = FUN__text__00469480(local_10);
            if (iVar1 == 0) {
              iVar1 = FUN__text__00469220(local_10);
              if (iVar1 == 0) {
                local_c[8] = local_c[8] + 1;
              }
              else {
                local_c[7] = local_c[7] + 1;
              }
            }
            else {
              local_c[6] = local_c[6] + 1;
            }
          }
        }
        else {
          iVar1 = FUN__text__00469eb0(local_10);
          if (iVar1 == 0) {
            iVar1 = FUN__text__00469f90(local_10);
            if (iVar1 == 0) goto LAB__text__004315e2;
            iVar1 = FUN__text__00469480(local_10);
            if (iVar1 == 0) {
              iVar1 = FUN__text__00469220(local_10);
              if (iVar1 == 0) {
                local_c[5] = local_c[5] + 1;
              }
              else {
                local_c[4] = local_c[4] + 1;
              }
            }
            else {
              local_c[3] = local_c[3] + 1;
            }
          }
          else {
            iVar1 = FUN__text__00469480(local_10);
            if (iVar1 == 0) {
              iVar1 = FUN__text__00469220(local_10);
              if (iVar1 == 0) {
                local_c[2] = local_c[2] + 1;
              }
              else {
                local_c[1] = local_c[1] + 1;
              }
            }
            else {
              *local_c = *local_c + 1;
            }
          }
        }
      }
      else {
        iVar1 = FUN__text__00469480(local_10);
        if (iVar1 == 0) {
          iVar1 = FUN__text__00469220(local_10);
          if (iVar1 == 0) {
            local_c[0x11] = local_c[0x11] + 1;
          }
          else {
            local_c[0x10] = local_c[0x10] + 1;
          }
        }
        else {
          local_c[0xf] = local_c[0xf] + 1;
        }
      }
    }
    local_14 = local_14 + 1;
  } while( true );
}

