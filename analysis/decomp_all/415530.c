
void __fastcall FUN__text__00415530(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int *local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0xb1d0) != 0) {
    local_10 = (int *)(param_1 + 0xb188);
    local_8 = param_1;
    if (*local_10 == 0 && *(int *)(param_1 + 0xb18c) == 0) {
      (*API_WINMM_DLL_timeGetTime)();
      uVar1 = FUN__text__0056ce80();
      *(undefined4 *)(local_8 + 0xb1e0) = uVar1;
      *(undefined4 *)(local_8 + 0xb1e4) = 0;
    }
    else {
      (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1 + 0xb1e0);
      local_c = FUN__text__0056ce80();
    }
  }
  local_8 = 0x4155c1;
  FUN__text__0056ce80();
  return;
}

