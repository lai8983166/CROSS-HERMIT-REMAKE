
void FUN__text__0045ada0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0042ae20("data\\plusdata.bin");
  if (local_c != 0) {
    FUN__text__00416790(local_c,0);
  }
  local_8 = 0x45adf1;
  FUN__text__0056ce80();
  return;
}

