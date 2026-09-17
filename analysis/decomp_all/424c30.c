
void __thiscall
FUN__text__00424c30(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 8) == 0) {
    if (*(int *)(param_1 + 0xc) == 0) {
      (*API_USER32_DLL_DefFrameProcA)(param_2,0,param_3,param_4,param_5);
      FUN__text__0056ce80();
    }
  }
  else {
    (*API_USER32_DLL_CallWindowProcA)(*(undefined4 *)(param_1 + 8),param_2,param_3,param_4,param_5);
    FUN__text__0056ce80();
  }
  local_8 = 0x424cb9;
  FUN__text__0056ce80();
  return;
}

