
void __fastcall FUN__text__0046b210(int param_1)

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
  local_10 = 0;
  local_8 = param_1;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if ((iVar1 != 0) &&
       (iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_c * 0x520), iVar1 != 0)) {
      local_10 = local_10 + 1;
    }
  }
  local_8 = 0x46b2b3;
  FUN__text__0056ce80();
  return;
}

