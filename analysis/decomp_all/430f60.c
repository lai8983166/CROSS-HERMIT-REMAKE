
void FUN__text__00430f60(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if (iVar1 == 0) {
    FUN__text__00430df0();
  }
  else {
    FUN__text__004313f0(local_8 + 0x115d14);
    local_c = FUN__text__00431890(local_8 + 0x115d14);
  }
  local_8 = 0x430fd0;
  FUN__text__0056ce80();
  return;
}

