
void FUN__text__0040a220(int param_1)

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
  FUN__text__0040b800(param_1);
  for (local_c = *(int *)(param_1 + 0x20); local_c != 0; local_c = *(int *)(local_c + 0x20)) {
    FUN__text__0040b800(local_c);
  }
  local_8 = 0x40a287;
  FUN__text__0056ce80();
  return;
}

