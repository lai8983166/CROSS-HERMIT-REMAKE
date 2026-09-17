
void FUN__text1__0083e283(HMODULE param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  char *local_110;
  char *local_10c;
  CHAR local_108;
  undefined4 local_107;
  
  if (param_1 == (HMODULE)0x0) {
    param_1 = GetModuleHandleA((LPCSTR)0x0);
  }
  local_108 = DAT_00874e88;
  puVar2 = &local_107;
  for (iVar1 = 0x40; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)puVar2 = 0;
  *(undefined1 *)((int)puVar2 + 2) = 0;
  GetModuleFileNameA(param_1,&local_108,0x104);
  local_10c = _strrchr(&local_108,0x5c);
  if (local_10c == (char *)0x0) {
    local_10c = &local_108;
  }
  local_110 = _strrchr(&local_108,0x2e);
  if ((local_110 == (char *)0x0) || (local_110 < local_10c)) {
    local_110 = _strchr(&local_108,0);
  }
  if (param_2 != 0) {
    FUN__text1__008491aa(local_110,&PTR_DAT_0086eda4,param_2);
    local_110 = _strchr(local_110,0);
  }
  FUN__text1__00848d20(local_110,".DbgLog");
  FUN__text1__00848d20
            ("F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\CROSS HERMIT-2.DbgLog",&local_108);
  return;
}

