
void FUN__text__00441de0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  undefined1 local_20 [13];
  undefined1 local_13;
  undefined1 local_10;
  undefined1 local_f;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00419450();
  if (iVar1 == 0) {
    _memset(local_20,0,0x14);
    local_13 = 3;
    local_10 = 0;
    local_f = FUN__text__0044ac50();
    local_24 = FUN__text__00419f90(local_20,0x14);
    if ((local_24 == 0) && (local_c = FUN__text__0041ade0(), local_c != 0)) {
      *(undefined1 *)(local_c + 1) = 1;
    }
  }
  local_8 = 0x441e97;
  FUN__text__0056ce80();
  return;
}

