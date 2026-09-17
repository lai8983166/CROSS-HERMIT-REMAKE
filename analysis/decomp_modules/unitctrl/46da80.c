
void __fastcall FUN__text__0046da80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 0xfa; local_10 = local_10 + 1) {
    local_c = local_8 + 0x80aec + local_10 * 0x520;
    iVar1 = FUN__text__00468d10(local_c);
    if (iVar1 != 0) {
      iVar1 = FUN__text__0046a430(local_c);
      if (iVar1 != 0) {
        FUN__text__0046db20(local_c,0);
        FUN__text__0046e0f0(local_c);
      }
    }
  }
  local_8 = 0x46db17;
  FUN__text__0056ce80();
  return;
}

