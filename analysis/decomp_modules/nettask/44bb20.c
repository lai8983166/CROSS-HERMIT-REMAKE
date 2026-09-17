
void __fastcall FUN__text__0044bb20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [16];
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  uint local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_20 = param_1 + 0x1a54;
  local_24 = param_1 + 0x1a88;
  local_8 = param_1;
  iVar1 = FUN__text__00419450();
  if ((iVar1 != 0) && (*(char *)(local_24 + 3) != '\x01')) {
    local_10 = 0;
    local_1c = *(uint *)(DAT_007a49fc + 0x199c) & 1;
    local_14 = 0x14;
    local_c = FUN__text__0044c710(&DAT_006065e0,0x14);
    if ((local_c != -1) && (local_1c != 0)) {
      FUN__text__004db2b0(5);
      local_28 = local_c / 5;
      local_2c = local_c % 5;
      if (*(char *)(local_20 + local_28 + 0x38) != (char)local_2c) {
        *(char *)(local_20 + local_28 + 0x38) = (char)local_2c;
        local_18 = FUN__text__004429a0();
      }
    }
  }
  local_8 = 0x44bc1f;
  FUN__text__0056ce80();
  return;
}

