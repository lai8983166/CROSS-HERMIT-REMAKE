
void FUN__text__0044a590(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00419450();
  if (iVar1 != 0) {
    local_10 = FUN__text__00449510(0);
    local_c = FUN__text__00449510(1);
    if (0x3f < local_c) {
      local_c = local_c + -0x40;
    }
    FUN__text__0044be10();
    FUN__text__004495a0();
    FUN__text__0044a640(0,local_10);
    FUN__text__0044a640(1,local_c);
  }
  FUN__text__0044a6e0();
  local_8 = 0x44a62e;
  FUN__text__0056ce80();
  return;
}

