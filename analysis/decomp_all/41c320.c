
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0041c320(undefined4 param_1,uint param_2,uint param_3,int param_4)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_184 [16];
  uint local_144;
  uint local_140;
  undefined *local_13c;
  undefined1 local_138 [13];
  undefined1 local_12b;
  undefined1 local_124 [13];
  undefined1 local_117;
  undefined *local_110;
  undefined1 local_10c [256];
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_184;
  for (iVar2 = 0x60; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_140 = param_2;
  if (param_2 < 0x112) {
    if (param_2 == 0x111) {
      local_144 = param_3 & 0xffff;
      if (local_144 == 2) {
        (*DAT_005923c4)(param_1,1);
        FUN__text__0056ce80();
      }
      else if (local_144 == 0x457) {
        iVar2 = FUN__text__00419450();
        if (iVar2 == 0) {
          _memset(local_138,0,0x14);
          local_12b = 3;
          local_c = FUN__text__00419f90(local_138,0x14);
          (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x184,0,0);
          uVar1 = FUN__text__0056ce80();
          (*API_USER32_DLL_SendMessageA)(uVar1);
          FUN__text__0056ce80();
          for (local_8 = 0; local_8 != *(char *)(DAT_00799b18 + 0x2000); local_8 = local_8 + 1) {
            if (*(int *)(DAT_00799b18 + 0x1804 + local_8 * 0x88) == *(int *)(DAT_00799b18 + 0x138))
            {
              *(undefined1 *)(DAT_00799b18 + 0x1781 + local_8 * 0x88) = 1;
            }
            if (*(char *)(DAT_00799b18 + 0x1781 + local_8 * 0x88) == '\0') {
              FUN__text__0056d810(local_10c,&DAT_00594448,DAT_00799b18 + 0x1782 + local_8 * 0x88);
            }
            else {
              FUN__text__0056d810(local_10c,&DAT_00594488,DAT_00799b18 + 0x1782 + local_8 * 0x88);
            }
            (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x180,0,local_10c);
            uVar1 = FUN__text__0056ce80();
            (*API_USER32_DLL_SendMessageA)(uVar1);
            FUN__text__0056ce80();
          }
          (*API_USER32_DLL_GetDlgItem)(param_1,0x457,0);
          uVar1 = FUN__text__0056ce80();
          (*API_USER32_DLL_EnableWindow)(uVar1);
          FUN__text__0056ce80();
          (*API_USER32_DLL_GetDlgItem)(param_1,2,0);
          uVar1 = FUN__text__0056ce80();
          (*API_USER32_DLL_EnableWindow)(uVar1);
          FUN__text__0056ce80();
          local_13c = &DAT_00594440;
          (*API_USER32_DLL_SetDlgItemTextA)(param_1,0x45b,&DAT_00594440);
          FUN__text__0056ce80();
          _DAT_00799b10 = 1;
        }
        else {
          _memset(local_124,0,0x14);
          local_117 = 3;
          local_c = FUN__text__00419fe0(local_124,0x14);
          (*DAT_005923c4)(param_1,0);
          FUN__text__0056ce80();
        }
      }
    }
    else if (param_2 == 2) {
      (*API_USER32_DLL_KillTimer)(param_1,1);
      FUN__text__0056ce80();
    }
    else if (param_2 == 0x110) {
      (*API_USER32_DLL_SetTimer)(param_1,1,100,0);
      FUN__text__0056ce80();
      DAT_00799b18 = param_4;
      (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x184,0,0);
      uVar1 = FUN__text__0056ce80();
      (*API_USER32_DLL_SendMessageA)(uVar1);
      FUN__text__0056ce80();
      iVar2 = FUN__text__00419450();
      if (iVar2 != 0) {
        FUN__text__0056d810(local_10c,&DAT_00594488,DAT_00799b18 + 0x1782);
        (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x180,0,local_10c);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_SendMessageA)(uVar1);
        FUN__text__0056ce80();
      }
      _DAT_00799b10 = 0;
      iVar2 = FUN__text__00419450();
      if (iVar2 == 0) {
        (*API_USER32_DLL_GetDlgItem)(param_1,0x457,1);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar1);
        FUN__text__0056ce80();
        (*API_USER32_DLL_GetDlgItem)(param_1,2,1);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar1);
        FUN__text__0056ce80();
      }
      else {
        local_110 = &DAT_00594458;
        (*API_USER32_DLL_SetDlgItemTextA)(param_1,0x45b,&DAT_00594458);
        FUN__text__0056ce80();
        (*API_USER32_DLL_GetDlgItem)(param_1,0x457,0);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar1);
        FUN__text__0056ce80();
        (*API_USER32_DLL_GetDlgItem)(param_1,2,0);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar1);
        FUN__text__0056ce80();
      }
    }
  }
  else if (param_2 == 0x113) {
    FUN__text__0041c830(param_1,0x113,param_3,param_4);
  }
  local_8 = 0x41c821;
  FUN__text__0056ce80();
  return;
}

