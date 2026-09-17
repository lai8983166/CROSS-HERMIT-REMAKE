
void __fastcall FUN__text__00425a50(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  (*API_KERNEL32_DLL_lstrlenA)(param_1 + 0x528);
  iVar1 = FUN__text__0056ce80();
  if (iVar1 == 0) {
    FUN__text__00426250();
    FUN__text__00426110();
    FUN__text__00426190();
  }
  uStack_c = 0x425ab7;
  FUN__text__0056ce80();
  return;
}

