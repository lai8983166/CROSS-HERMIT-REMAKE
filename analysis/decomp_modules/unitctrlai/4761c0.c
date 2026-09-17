
void FUN__text__004761c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  char local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = *local_10;
  if (local_14 == '\0') {
    FUN__text__0046b0f0(param_1,1);
    FUN__text__0046b0b0(param_1,1);
    FUN__text__0046bcc0(param_1,1);
    *local_10 = *local_10 + '\x01';
  }
  local_8 = 0x476247;
  FUN__text__0056ce80();
  return;
}

