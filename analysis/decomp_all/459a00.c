
void FUN__text__00459a00(void)

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
  FUN__text__0045a230(10);
  do {
    local_10 = *(int *)(local_8 + 0x30);
    if (local_10 == 0) {
      local_c = FUN__text__00459b10();
    }
    else if (local_10 == 1) {
      local_c = FUN__text__00459e00();
    }
    else if (local_10 == 2) {
      DAT_007a46ac = 0;
      FUN__text__00422360(0);
      local_c = 1;
    }
  } while (local_c == 0);
  local_8 = 0x459abb;
  FUN__text__0056ce80();
  return;
}

