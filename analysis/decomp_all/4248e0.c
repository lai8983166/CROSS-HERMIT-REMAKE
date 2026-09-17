
void __fastcall FUN__text__004248e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 4) != 0) {
    local_8 = param_1;
    if (*(int *)(param_1 + 8) != 0) {
      local_c = (-(uint)(*(int *)(param_1 + 0xc) != 0) & 8) - 4;
      (*API_USER32_DLL_SetWindowLongA)
                (*(undefined4 *)(param_1 + 4),local_c,*(undefined4 *)(param_1 + 8));
      FUN__text__0056ce80();
    }
    (*API_USER32_DLL_RemovePropA)(*(undefined4 *)(local_8 + 4),"CPP_CLASS");
    FUN__text__0056ce80();
  }
  local_8 = 0x424974;
  FUN__text__0056ce80();
  return;
}

