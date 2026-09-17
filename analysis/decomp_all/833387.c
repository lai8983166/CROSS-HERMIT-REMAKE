
undefined1 __thiscall FUN__text1__00833387(int param_1,int param_2,int param_3)

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
    if ((param_2 != 0) && (0 < param_3)) {
      FUN__text1__0084906b(param_2,puVar1[1],param_3);
      *(undefined2 *)(param_2 + -2 + param_3 * 2) = 0;
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

