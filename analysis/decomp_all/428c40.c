
void __thiscall FUN__text__00428c40(int *param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [12];
  undefined4 uStack_1c;
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*param_1 != 0) {
    FUN__text__00428e00();
  }
  (*API_ADVAPI32_DLL_RegOpenKeyExA)(param_2,param_3,0,0xf003f,local_8);
  local_c = FUN__text__0056ce80();
  if (local_c != 0) {
    FUN__text__004292e0(local_c);
  }
  uStack_1c = 0x428cba;
  FUN__text__0056ce80();
  return;
}

