
void FUN__text__0047efb0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  char local_18;
  int local_14;
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
  local_14 = FUN__text__0047a8e0(param_1);
  local_18 = *local_10;
  if (local_18 == '\0') {
    FUN__text__0046bcc0(param_1,1);
    *local_10 = *local_10 + '\x01';
  }
  else if ((local_18 == '\x01') &&
          (*(int *)(local_14 + 0x38) = *(int *)(local_14 + 0x38) + -1, *(int *)(local_14 + 0x38) < 1
          )) {
    *(undefined4 *)(local_14 + 0x38) = 0;
    iVar1 = FUN__text__0047f090(param_1);
    if (iVar1 == 0) {
      FUN__text__00475270(param_1,4);
    }
    else {
      FUN__text__00475270(param_1,0xf);
    }
  }
  local_8 = 0x47f082;
  FUN__text__0056ce80();
  return;
}

