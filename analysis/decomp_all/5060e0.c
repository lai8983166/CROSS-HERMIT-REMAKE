
void FUN__text__005060e0(void)

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
  local_c = FUN__text__0042ae20("data\\op\\opdata.bin");
  if (local_c != 0) {
    FUN__text__00416790(local_c,0);
    local_10 = local_c;
    FUN__text__00428ad0(local_c);
  }
  local_8 = 0x506143;
  FUN__text__0056ce80();
  return;
}

