
void FUN__text__0042a9c0(char *param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_2a0 [16];
  int local_260;
  undefined4 local_25c;
  char local_258 [260];
  undefined4 local_154;
  undefined4 local_150;
  undefined4 local_14c;
  uint local_148 [79];
  undefined4 uStack_c;
  int local_8;
  
  puVar3 = local_2a0;
  for (iVar2 = 0xa7; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = 0;
  local_25c = 0;
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_260 = FUN__text__0056ce80();
  _memset(local_258,0,0x104);
  if (((local_260 != 0) && (*param_1 != '.')) && (iVar2 = FUN__text__0042a030(param_1), iVar2 == 0))
  {
    for (; local_25c < local_260; local_25c = local_25c + 1) {
      for (; (local_25c < local_260 &&
             ((param_1[local_25c] != '\\' || ((0 < local_25c && (local_258[local_25c + -1] == ':')))
              ))); local_25c = local_25c + 1) {
        local_258[local_25c] = param_1[local_25c];
      }
      local_258[local_25c] = '\0';
      (*DAT_005921f4)(local_258,local_148);
      local_8 = FUN__text__0056ce80();
      if (local_8 == -1) {
        local_154 = 0xc;
        local_150 = 0;
        local_14c = 0;
        (*API_KERNEL32_DLL_CreateDirectoryA)(local_258,&local_154);
        uVar1 = FUN__text__0056ce80();
      }
      else {
        (*API_KERNEL32_DLL_FindClose)(local_8);
        FUN__text__0056ce80();
        uVar1 = local_148[0] & 0x10;
      }
      if (uVar1 == 0) break;
      local_258[local_25c] = '\\';
    }
  }
  uStack_c = 0x42abb3;
  FUN__text__0056ce80();
  return;
}

