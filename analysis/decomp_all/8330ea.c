
void __thiscall FUN__text1__008330ea(int param_1,char *param_2)

{
  size_t sVar1;
  void *pvVar2;
  undefined4 *local_18;
  
  EnterCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x10));
  local_18 = operator_new(0xc);
  if (local_18 == (undefined4 *)0x0) {
    local_18 = (undefined4 *)0x0;
  }
  else {
    local_18[1] = 0;
    sVar1 = _strlen(param_2);
    pvVar2 = operator_new(sVar1 + 1);
    *local_18 = pvVar2;
    FUN__text1__00848d20(*local_18,param_2);
    local_18[2] = 0;
  }
  if (*(int *)(param_1 + 0xc) == 0) {
    *(undefined4 **)(param_1 + 0xc) = local_18;
    *(undefined4 **)(param_1 + 8) = local_18;
  }
  else {
    *(undefined4 **)(*(int *)(param_1 + 0xc) + 8) = local_18;
    *(undefined4 *)(param_1 + 0xc) = *(undefined4 *)(*(int *)(param_1 + 0xc) + 8);
  }
  LeaveCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x10));
  return;
}

