
void FUN__text__00426310(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_c = FUN__text__0056ce80();
  if (local_c < 0x3f) {
    (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0x63c,param_1);
    FUN__text__0056ce80();
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff684 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = 0x4263a2;
  FUN__text__0056ce80();
  return;
}

