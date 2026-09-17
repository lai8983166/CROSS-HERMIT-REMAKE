
void __thiscall FUN__text__0041c9d0(int param_1,undefined4 param_2,int *param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_a04 [16];
  char local_9c4;
  int local_9c0;
  undefined *local_9bc;
  int local_9b8;
  int local_9b4;
  undefined1 local_9b0 [13];
  undefined1 local_9a3;
  undefined1 local_9a0;
  int local_11c;
  int *local_118;
  undefined1 local_114 [256];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_a04;
  for (iVar3 = 0x280; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (*param_3 == 0) {
    local_118 = (int *)param_3[2];
    local_9c0 = *local_118;
    if (local_9c0 == 3) {
      local_11c = param_3[2];
      FUN__text__0041afd0(*(undefined4 *)(local_11c + 0x20),*(undefined4 *)(local_11c + 8));
      (*API_USER32_DLL_GetDlgItem)(param_2,0x3f8,0x184,0,0);
      uVar2 = FUN__text__0056ce80();
      (*API_USER32_DLL_SendMessageA)(uVar2);
      FUN__text__0056ce80();
      for (local_10 = 0; local_10 != *(char *)(local_8 + 0x2000); local_10 = local_10 + 1) {
        if (*(char *)(local_8 + 0x1781 + local_10 * 0x88) == '\0') {
          FUN__text__0056d810(local_114,&DAT_00594448,local_8 + 0x1782 + local_10 * 0x88);
        }
        else {
          FUN__text__0056d810(local_114,&DAT_00594488,local_8 + 0x1782 + local_10 * 0x88);
        }
        (*API_USER32_DLL_GetDlgItem)(param_2,0x3f8,0x180,0,local_114);
        uVar2 = FUN__text__0056ce80();
        (*API_USER32_DLL_SendMessageA)(uVar2);
        FUN__text__0056ce80();
      }
      _memset(local_9b0,0,0x894);
      local_9a3 = 2;
      local_9a0 = *(undefined1 *)(local_8 + 0x2000);
      for (local_10 = 0; local_10 != *(char *)(local_8 + 0x2000); local_10 = local_10 + 1) {
      }
      local_c = FUN__text__00419fe0(local_9b0,0x894);
      if ((local_c != 0) &&
         (iVar3 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff5a0 + 0x21,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  else {
    local_9b4 = param_3[2];
    local_9c4 = *(char *)(local_9b4 + 0xd);
    if (local_9c4 == '\x02') {
      local_9b8 = param_3[2];
    }
    else if (local_9c4 == '\x03') {
      for (local_10 = 0; local_10 != *(char *)(param_1 + 0x2000); local_10 = local_10 + 1) {
        if (*param_3 == *(int *)(param_1 + 0x1804 + local_10 * 0x88)) {
          *(undefined1 *)(param_1 + 0x1781 + local_10 * 0x88) = 1;
        }
      }
      (*API_USER32_DLL_GetDlgItem)(param_2,0x3f8,0x184,0,0);
      uVar2 = FUN__text__0056ce80();
      (*API_USER32_DLL_SendMessageA)(uVar2);
      FUN__text__0056ce80();
      for (local_10 = 0; local_10 != *(char *)(local_8 + 0x2000); local_10 = local_10 + 1) {
        if (*(char *)(local_8 + 0x1781 + local_10 * 0x88) == '\0') {
          FUN__text__0056d810(local_114,&DAT_00594448,local_8 + 0x1782 + local_10 * 0x88);
        }
        else {
          FUN__text__0056d810(local_114,&DAT_00594488,local_8 + 0x1782 + local_10 * 0x88);
        }
        (*API_USER32_DLL_GetDlgItem)(param_2,0x3f8,0x180,0,local_114);
        uVar2 = FUN__text__0056ce80();
        (*API_USER32_DLL_SendMessageA)(uVar2);
        FUN__text__0056ce80();
      }
      local_14 = 0;
      for (local_10 = 0; local_10 != *(char *)(local_8 + 0x2000); local_10 = local_10 + 1) {
        if (*(char *)(local_8 + 0x1781 + local_10 * 0x88) != '\0') {
          local_14 = local_14 + 1;
        }
      }
      if (local_14 == *(char *)(local_8 + 0x2000)) {
        local_9bc = &DAT_00594498;
        (*API_USER32_DLL_SetDlgItemTextA)(param_2,0x45b,&DAT_00594498);
        FUN__text__0056ce80();
        (*API_USER32_DLL_GetDlgItem)(param_2,0x457,1);
        uVar2 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar2);
        FUN__text__0056ce80();
        (*API_USER32_DLL_GetDlgItem)(param_2,2,1);
        uVar2 = FUN__text__0056ce80();
        (*API_USER32_DLL_EnableWindow)(uVar2);
        FUN__text__0056ce80();
      }
    }
  }
  local_8 = 0x41ce54;
  FUN__text__0056ce80();
  return;
}

