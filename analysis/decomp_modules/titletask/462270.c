
void __fastcall FUN__text__00462270(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0x179;
  local_10 = 0x144;
  local_8 = param_1;
  while ((local_14 = FUN__text__004623b0(local_c,local_10), local_14 == -1 ||
         ((*(uint *)(DAT_007a49fc + 0x199c) & 1) == 0))) {
    FUN__text__004627a0();
    FUN__text__00462a90(local_c,local_10);
    if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) {
      FUN__text__00462b90(local_c,local_10,local_14);
    }
    FUN__text__00462d10();
    FUN__text__00422360(0);
  }
  FUN__text__004db2b0(0);
  local_18 = 4;
  do {
    FUN__text__004627a0();
    FUN__text__00462a90(local_c,local_10);
    FUN__text__00462b90(local_c,local_10,local_14);
    FUN__text__00462d10();
    FUN__text__00422360(0);
    local_18 = local_18 + -1;
  } while (local_18 != 0);
  local_8 = 0x4623a6;
  FUN__text__0056ce80();
  return;
}

