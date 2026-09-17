
void __thiscall FUN__text__0040db10(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 8) = param_2;
  local_8 = param_1;
  local_c = FUN__text__00428a40(*(int *)(param_1 + 8) << 3);
  *(undefined4 *)(local_8 + 0x10) = local_c;
  if (*(int *)(local_8 + 0x10) != 0) {
    FUN__text__0040db90();
  }
  local_8 = 0x40db7b;
  FUN__text__0056ce80();
  return;
}

