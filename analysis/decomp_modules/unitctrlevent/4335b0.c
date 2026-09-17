
void FUN__text__004335b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__004e2720(2,0);
  local_c = local_10;
  if (local_10 == 0) {
    iVar1 = FUN__text__004551c0(0,0x14);
    if (iVar1 != 0) {
      FUN__text__004549d0(0,0,0x14,0,0,1,1);
      local_c = local_c + 1;
      FUN__text__004e29a0(2,0,local_c);
    }
  }
  else if (local_10 == 1) {
    iVar1 = FUN__text__004551c0(0,0x15);
    if (iVar1 != 0) {
      FUN__text__004549d0(0,0,0x15,0,0,1,1);
      local_c = local_c + 1;
      FUN__text__004e29a0(2,0,local_c);
    }
  }
  else if (((local_10 == 2) && (iVar1 = FUN__text__004307b0(), iVar1 == 0)) &&
          (iVar1 = FUN__text__004551c0(0,0x16), iVar1 != 0)) {
    FUN__text__004549d0(0,0,0x16,0,0,1,1);
    local_c = local_c + 1;
    FUN__text__004e29a0(2,0,local_c);
  }
  local_8 = 0x433718;
  FUN__text__0056ce80();
  return;
}

