
void __fastcall FUN__text__00426040(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [17];
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 8) != 0) {
    local_8 = param_1;
    (*API_KERNEL32_DLL_lstrlenA)(param_1 + 0x528);
    FUN__text__0056ce80();
  }
  local_8 = 0x42609e;
  FUN__text__0056ce80();
  return;
}

