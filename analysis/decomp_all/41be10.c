
void FUN__text__0041be10(undefined4 param_1,int param_2,uint param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_258 [16];
  uint local_218;
  int local_214;
  undefined1 local_210 [256];
  undefined1 local_110 [256];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_258;
  for (iVar1 = 0x95; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_214 = param_2;
  if (param_2 == 0x110) {
    (*API_USER32_DLL_SetDlgItemTextA)(param_1,0x405,&DAT_00594430);
    FUN__text__0056ce80();
    (*API_USER32_DLL_SetDlgItemTextA)(param_1,0x45a,&DAT_00594420);
    FUN__text__0056ce80();
    DAT_00799b14 = param_4;
  }
  else if (param_2 == 0x111) {
    local_218 = param_3 & 0xffff;
    if (local_218 < 0x459) {
      if (local_218 == 0x458) {
        local_c = FUN__text__004187b0();
        if (local_c == 0) {
          (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8);
          local_10 = FUN__text__0056ce80();
          if (local_10 != 0) {
            (*API_USER32_DLL_SendMessageA)(local_10,0x184,0,0);
            local_c = FUN__text__0056ce80();
            for (local_8 = 0; local_8 != *(int *)(DAT_00799b14 + 0x244); local_8 = local_8 + 1) {
              (*API_USER32_DLL_SendMessageA)
                        (local_10,0x181,local_8,
                         *(undefined4 *)(DAT_00799b14 + 0x280 + local_8 * 0x54));
              FUN__text__0056ce80();
            }
            if (*(int *)(DAT_00799b14 + 0x244) != 0) {
              (*API_USER32_DLL_SendMessageA)(local_10,0x186,0,0);
              local_c = FUN__text__0056ce80();
            }
          }
        }
        else {
          (*DAT_005923d8)(param_1,&DAT_00594404,&DAT_00594414,0);
          FUN__text__0056ce80();
        }
      }
      else if (local_218 == 2) {
        (*DAT_005923c4)(param_1,2);
        FUN__text__0056ce80();
      }
      else if (local_218 == 0x444) {
        (*API_USER32_DLL_GetDlgItemTextA)(param_1,0x405,local_110,0xfc);
        local_c = FUN__text__0056ce80();
        if (local_c == 0) {
          local_c = 0;
        }
        else {
          (*API_USER32_DLL_GetDlgItemTextA)(param_1,0x45a,local_210,0xfc);
          local_c = FUN__text__0056ce80();
          if (local_c != 0) {
            (*API_KERNEL32_DLL_lstrlenA)(local_110);
            iVar1 = FUN__text__0056ce80();
            if (iVar1 != 0) {
              (*API_KERNEL32_DLL_lstrlenA)(local_210);
              iVar1 = FUN__text__0056ce80();
              if ((iVar1 != 0) && (iVar1 = FUN__text__00418f70(local_110,4,1), iVar1 == 0)) {
                iVar1 = FUN__text__00419950(local_210);
                if (iVar1 == 0) {
                  (*DAT_005923c4)(param_1,0);
                  FUN__text__0056ce80();
                }
                else {
                  FUN__text__00419240();
                  (*DAT_005923c4)(param_1,0xffffffff);
                  FUN__text__0056ce80();
                }
              }
            }
          }
        }
      }
    }
    else if (local_218 == 0x459) {
      (*API_USER32_DLL_GetDlgItemTextA)(param_1,0x45a,local_210,0xfc);
      local_c = FUN__text__0056ce80();
      if (local_c != 0) {
        (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8);
        local_10 = FUN__text__0056ce80();
        if (local_10 != 0) {
          (*API_USER32_DLL_SendMessageA)(local_10,0x188,0,0);
          local_c = FUN__text__0056ce80();
          if ((local_c != -1) && (local_c < *(int *)(DAT_00799b14 + 0x244))) {
            iVar1 = FUN__text__004190f0(local_c,1);
            if (iVar1 == 0) {
              iVar1 = FUN__text__004199a0(local_210,0);
              if (iVar1 == 0) {
                (*DAT_005923c4)(param_1,1);
                FUN__text__0056ce80();
              }
              else {
                (*DAT_005923d8)(param_1,&DAT_005943cc,&DAT_005943dc,0);
                FUN__text__0056ce80();
                FUN__text__00419240();
                (*DAT_005923c4)(param_1,0xffffffff);
                FUN__text__0056ce80();
              }
            }
            else {
              (*DAT_005923d8)(param_1,&DAT_005943e8,&DAT_005943f8,0);
              FUN__text__0056ce80();
              (*DAT_005923c4)(param_1,0xffffffff);
              FUN__text__0056ce80();
            }
          }
        }
      }
    }
  }
  local_8 = 0x41c2a1;
  FUN__text__0056ce80();
  return;
}

