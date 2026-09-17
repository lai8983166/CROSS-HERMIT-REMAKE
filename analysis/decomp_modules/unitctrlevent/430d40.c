
void __fastcall FUN__text__00430d40(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int *)(param_1 + 0xdc8ec);
  local_14 = 0;
  local_8 = param_1;
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    iVar1 = FUN__text__00468d10(local_c[local_10 + 1]);
    if (iVar1 != 0) {
      iVar1 = FUN__text__0046a550(local_c[local_10 + 1]);
      if (iVar1 != 0) {
        iVar1 = FUN__text__00469ad0(local_c[local_10 + 1]);
        if (iVar1 == 0) {
          local_14 = local_14 + 1;
        }
      }
    }
  }
  local_8 = 0x430deb;
  FUN__text__0056ce80();
  return;
}

