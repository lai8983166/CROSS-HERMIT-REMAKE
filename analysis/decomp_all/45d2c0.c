
/* WARNING: Removing unreachable block (ram,0x0045d428) */

void __fastcall FUN__text__0045d2c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  byte local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__00415ed0(param_1 + 0x30,&DAT_0059adc8,1,1);
  local_14 = 7;
  FUN__text__00416d20(DAT_007a49fc + 0xb408,0,7);
  FUN__text__00422360(0);
  local_c = 0;
  local_10 = 1;
  do {
    local_c = local_c + local_10;
    if (0x1ff < (int)local_c) {
      local_10 = -local_10;
    }
    if ((int)local_c < 1) {
      local_10 = -local_10;
    }
    FUN__text__00416d20(DAT_007a49fc + 0xb408,local_c & 0xffff,
                        CONCAT31((int3)(local_c >> 8),local_14));
    FUN__text__00416cc0(DAT_007a49fc + 0xb408);
    FUN__text__004079c0(0,0);
    FUN__text__00422360(0);
    iVar1 = FUN__text__004128f0(0x4f,1);
    if (iVar1 != 0) {
      local_14 = local_14 ^ 4;
    }
    iVar1 = FUN__text__004128f0(0x50,1);
    if (iVar1 != 0) {
      local_14 = local_14 ^ 2;
    }
    iVar1 = FUN__text__004128f0(0x51,1);
    if (iVar1 != 0) {
      local_14 = local_14 ^ 1;
    }
  } while( true );
}

