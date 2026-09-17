
void FUN__text__004478e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0044bd70();
  FUN__text__004495a0();
  FUN__text__00449fd0();
  FUN__text__0044b950((int)*(char *)(local_8 + 0x1a8b));
  FUN__text__0044a960();
  FUN__text__0044aaf0();
  FUN__text__0044b610();
  *(undefined1 *)(local_8 + 0x1aa2) = 0;
  FUN__text__00425a10();
  FUN__text__004262a0(0x3a);
  FUN__text__00425ed0(1);
  FUN__text__00422360(0);
  iVar1 = FUN__text__00419450();
  if (iVar1 != 0) {
    FUN__text__004192e0(1);
  }
  if (*(int *)(local_8 + 0x30) == 1) {
    FUN__text__0041b190();
    local_14 = FUN__text__0041ade0();
    (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0x1a60,local_14 + 2);
    FUN__text__0056ce80();
    iVar1 = FUN__text__00419450();
    if (iVar1 == 0) {
      FUN__text__00442eb0();
    }
    else {
      FUN__text__00442db0();
      FUN__text__00442b30();
      FUN__text__00441fe0();
      FUN__text__004429a0();
    }
  }
  FUN__text__00447ac0();
  local_c = FUN__text__00447d00();
  FUN__text__00447be0();
  FUN__text__00425ed0(0);
  FUN__text__00422360(0);
  local_18 = local_c;
  if (local_c == 3) {
    local_10 = FUN__text__00419240();
  }
  local_8 = 0x447aae;
  FUN__text__0056ce80();
  return;
}

