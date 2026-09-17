
void FUN__text__0041ce60(undefined4 param_1,int *param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_160 [16];
  char local_120;
  undefined4 local_11c;
  int local_118;
  int local_114;
  undefined4 *local_110;
  undefined1 local_10c [256];
  int local_c;
  int local_8;
  
  puVar3 = local_160;
  for (iVar2 = 0x57; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*param_2 == 0) {
    local_110 = (undefined4 *)param_2[2];
    local_11c = *local_110;
  }
  else {
    local_114 = param_2[2];
    local_120 = *(char *)(local_114 + 0xd);
    if (local_120 == '\x02') {
      local_118 = param_2[2];
      FUN__text__0041ab10();
      for (local_c = 0; local_c != *(char *)(local_118 + 0x10); local_c = local_c + 1) {
      }
      (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x184,0,0);
      uVar1 = FUN__text__0056ce80();
      (*API_USER32_DLL_SendMessageA)(uVar1);
      FUN__text__0056ce80();
      for (local_c = 0; local_c != *(char *)(local_8 + 0x2000); local_c = local_c + 1) {
        if (*(char *)(local_8 + 0x1781 + local_c * 0x88) == '\0') {
          FUN__text__0056d810(local_10c,&DAT_00594448,local_8 + 0x1782 + local_c * 0x88);
        }
        else {
          FUN__text__0056d810(local_10c,&DAT_00594488,local_8 + 0x1782 + local_c * 0x88);
        }
        (*API_USER32_DLL_GetDlgItem)(param_1,0x3f8,0x180,0,local_10c);
        uVar1 = FUN__text__0056ce80();
        (*API_USER32_DLL_SendMessageA)(uVar1);
        FUN__text__0056ce80();
      }
    }
  }
  local_8 = 0x41d02d;
  FUN__text__0056ce80();
  return;
}

