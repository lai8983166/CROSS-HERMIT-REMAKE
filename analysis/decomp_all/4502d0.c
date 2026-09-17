
void __fastcall FUN__text__004502d0(int param_1)

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
  if (*(int *)(param_1 + 0x1108) != 0) {
    local_8 = param_1;
    (*API_KERNEL32_DLL_lstrlenA)(*(undefined4 *)(param_1 + 0x1108));
    iVar1 = FUN__text__0056ce80();
    if (iVar1 != 0) {
      FUN__text__0042a8e0(*(undefined4 *)(local_8 + 0x1108));
    }
  }
  local_8 = 0x45034a;
  FUN__text__0056ce80();
  return;
}

