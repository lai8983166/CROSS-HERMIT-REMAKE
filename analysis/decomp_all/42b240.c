
void FUN__text__0042b240(int param_1)

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
  if (param_1 == 1) {
    do {
      (*API_USER32_DLL_ShowCursor)(1);
      local_8 = FUN__text__0056ce80();
    } while (local_8 < 0);
  }
  else {
    do {
      (*API_USER32_DLL_ShowCursor)(0);
      local_8 = FUN__text__0056ce80();
    } while (-1 < local_8);
  }
  local_8 = 0x42b2bd;
  FUN__text__0056ce80();
  return;
}

