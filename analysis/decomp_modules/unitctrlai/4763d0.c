
void FUN__text__004763d0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  char local_18;
  char local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = *local_10;
  if (local_14 == '\0') {
    FUN__text__0046bcc0(param_1,0x18);
    *local_10 = *local_10 + '\x01';
  }
  else if (local_14 != '\x01') goto LAB__text__0047645b;
  local_18 = *(char *)(*(int *)(param_1 + 600) + 0x9f);
  if (local_18 != '\x03') {
    FUN__text__00475270(param_1,0xf);
  }
LAB__text__0047645b:
  local_8 = 0x47646a;
  FUN__text__0056ce80();
  return;
}

