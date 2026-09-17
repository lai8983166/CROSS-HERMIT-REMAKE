
void FUN__text__0047e240(undefined4 param_1)

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
  local_c = FUN__text__0047a8e0(param_1);
  *(int *)(local_c + 0x2c) = *(int *)(local_c + 0x2c) + 1;
  if (*(int *)(local_c + 4) <= *(int *)(local_c + 0x2c)) {
    *(undefined4 *)(local_c + 0x2c) = 0;
  }
  local_8 = 0x47e2a9;
  FUN__text__0056ce80();
  return;
}

