
void FUN__text__004538d0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if (iVar1 == 0) {
    *(undefined4 *)(local_8 + 0x34) = 2;
  }
  else {
    *(undefined4 *)(local_8 + 0x34) = 1;
  }
  local_8 = 0x45391e;
  FUN__text__0056ce80();
  return;
}

