
undefined1 __thiscall FUN__text1__008331bc(int param_1,char *param_2,size_t param_3)

{
  undefined4 *puVar1;
  undefined1 local_8;
  
  EnterCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x10));
  local_8 = 0;
  if (*(int *)(param_1 + 8) != 0) {
    puVar1 = *(undefined4 **)(param_1 + 8);
    *(undefined4 *)(param_1 + 8) = puVar1[2];
    if (*(int *)(param_1 + 8) == 0) {
      *(undefined4 *)(param_1 + 0xc) = 0;
    }
    if ((param_2 != (char *)0x0) && (0 < (int)param_3)) {
      _strncpy(param_2,(char *)*puVar1,param_3);
      param_2[param_3 - 1] = '\0';
    }
    if (puVar1 != (undefined4 *)0x0) {
      FUN__text1__00848476(*puVar1);
      FUN__text1__00848476(puVar1[1]);
      FUN__text1__00848476(puVar1);
    }
    local_8 = 1;
  }
  LeaveCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x10));
  return local_8;
}

