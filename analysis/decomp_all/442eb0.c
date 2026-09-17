
void FUN__text__00442eb0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined1 local_18 [13];
  undefined1 local_b;
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00419450();
  if (iVar1 == 0) {
    _memset(local_18,0,0x10);
    local_b = 0xe;
    local_1c = FUN__text__00419f90(local_18,0x10);
  }
  local_8 = 0x442f30;
  FUN__text__0056ce80();
  return;
}

