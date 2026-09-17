
void __thiscall
FUN__text__00428e80(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    (*API_ADVAPI32_DLL_RegQueryValueExA)(*param_1,param_2,0,param_3,param_4,param_5);
    local_c = FUN__text__0056ce80();
    if (local_c != 0) {
      FUN__text__004292e0(local_c);
    }
  }
  local_8 = (int *)0x428efb;
  FUN__text__0056ce80();
  return;
}

