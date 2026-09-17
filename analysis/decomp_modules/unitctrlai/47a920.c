
void FUN__text__0047a920(undefined4 param_1)

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
  local_c = FUN__text__0047a8e0(param_1);
  *(int *)(local_c + 0x28) = *(int *)(local_c + 0x28) + 1;
  if (*(int *)(local_c + 0xc) <= *(int *)(local_c + 0x28)) {
    *(undefined4 *)(local_c + 0x28) = 0;
    local_10 = FUN__text__0047ac80(param_1);
    if ((local_10 == 0) && (local_10 = FUN__text__0047a9d0(param_1), local_10 != 0)) {
      FUN__text__0047b2c0(param_1,local_10);
    }
  }
  local_8 = 0x47a9c6;
  FUN__text__0056ce80();
  return;
}

