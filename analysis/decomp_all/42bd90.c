
void __fastcall FUN__text__0042bd90(int param_1)

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
  if (*(int *)(param_1 + 4) != 0) {
    local_8 = param_1;
    (*API_USER32_DLL_UnhookWindowsHookEx)(*(undefined4 *)(param_1 + 4));
    FUN__text__0056ce80();
  }
  local_8 = 0x42bdd9;
  FUN__text__0056ce80();
  return;
}

