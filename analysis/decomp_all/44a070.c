
void __fastcall FUN__text__0044a070(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  uint local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_20 = param_1 + 0x1a54;
  local_14 = 0;
  local_18 = (int)*(char *)(param_1 + 0x1a8a);
  local_c = param_1 + 0x8a80 + local_18 * 8;
  local_1c = *(uint *)(DAT_007a49fc + 0x199c) & 1;
  local_8 = param_1;
  local_10 = FUN__text__0044c710(&DAT_00605e78,8);
  if (local_10 != -1) {
    if (local_1c != 0) {
      local_24 = local_10;
      switch(local_10) {
      case 0:
        FUN__text__00428720();
        FUN__text__004db2b0(5);
        break;
      case 1:
        FUN__text__00428810();
        FUN__text__004db2b0(5);
        break;
      case 2:
        FUN__text__00428850();
        FUN__text__004db2b0(5);
        break;
      case 3:
        FUN__text__00428760();
        FUN__text__004db2b0(5);
        break;
      case 4:
      case 5:
      case 6:
      case 7:
        local_18 = local_10 + -4;
        if (local_18 != *(char *)(local_20 + 0x36)) {
          *(undefined1 *)(local_20 + 0x36) = (undefined1)local_18;
          FUN__text__0044c560((int)*(short *)(local_20 + 0x34),(int)*(char *)(local_20 + 0x36),
                              *(undefined4 *)(local_8 + 0x1ba4));
          FUN__text__004db2b0(5);
        }
      }
    }
    local_14 = 1;
  }
  if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
    local_10 = -1;
  }
  FUN__text__0044a210(local_10);
  local_8 = 0x44a1e3;
  FUN__text__0056ce80();
  return;
}

