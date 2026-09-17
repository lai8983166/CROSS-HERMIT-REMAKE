
void __fastcall FUN__text__00415930(int param_1)

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
  if (*(int *)(param_1 + 0xb1d0) != 0) {
    do {
      iVar1 = FUN__text__00415990();
    } while (iVar1 == 0);
  }
  local_8 = 0x415981;
  FUN__text__0056ce80();
  return;
}

