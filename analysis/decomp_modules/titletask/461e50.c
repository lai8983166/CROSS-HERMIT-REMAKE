
void __fastcall FUN__text__00461e50(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0xe4c;
  local_8 = param_1;
  do {
    local_14 = local_14 + -1;
    if (local_14 == 0) {
      local_10 = 6;
LAB__text__00461f53:
      local_8 = 0x461f67;
      FUN__text__0056ce80();
      return;
    }
    local_10 = FUN__text__004626b0();
    if ((local_10 != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
      FUN__text__004db2b0(0);
      local_c = 8;
      do {
        FUN__text__004627a0();
        FUN__text__00462d10();
        FUN__text__00462910(local_10);
        FUN__text__00422360(0);
        local_c = local_c + -1;
      } while (local_c != 0);
      local_c = 0;
      goto LAB__text__00461f53;
    }
    FUN__text__004627a0();
    FUN__text__00462d10();
    if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) {
      FUN__text__00462910(local_10);
    }
    FUN__text__00422360(0);
  } while( true );
}

