
void FUN__text__0040dab0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0040db10(0x1000);
  if (iVar1 == 0) {
    FUN__text__0040dbf0(0x100000);
  }
  local_8 = 0x40db0c;
  FUN__text__0056ce80();
  return;
}

