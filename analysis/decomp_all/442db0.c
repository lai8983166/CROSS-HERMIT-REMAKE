
void FUN__text__00442db0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  undefined4 local_20;
  int local_1c;
  undefined1 local_18 [13];
  undefined1 local_b;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00419450();
  if (iVar1 != 0) {
    local_1c = FUN__text__0041ae70();
    *(undefined1 *)(local_1c + 1) = 1;
    _memset(local_18,0,0x10);
    local_b = 0xc;
    local_20 = FUN__text__00419fe0(local_18,0x10);
  }
  local_8 = 0x442e4b;
  FUN__text__0056ce80();
  return;
}

