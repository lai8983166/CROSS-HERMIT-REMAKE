
void FUN__text__004295c0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_GetLastError)();
  local_8 = FUN__text__0056ce80();
  if (local_8 != 0) {
    (*DAT_00592204)(0x1300,0,local_8,0x400,&local_c,0,0);
    local_10 = FUN__text__0056ce80();
    if ((local_10 != 0) && (FUN__text__0042b2d0(&DAT_00592f50,local_c), local_c != 0)) {
      (*API_KERNEL32_DLL_LocalFree)(local_c);
      FUN__text__0056ce80();
    }
  }
  local_8 = 0x429660;
  FUN__text__0056ce80();
  return;
}

