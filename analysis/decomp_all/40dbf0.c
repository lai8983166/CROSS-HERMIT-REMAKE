
void __thiscall FUN__text__0040dbf0(int param_1,undefined4 param_2)

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
  *(undefined4 *)(param_1 + 0xc) = param_2;
  local_8 = param_1;
  local_c = FUN__text__00428a40(*(undefined4 *)(param_1 + 0xc));
  *(undefined4 *)(local_8 + 0x14) = local_c;
  if (*(int *)(local_8 + 0x14) != 0) {
    _memset(*(void **)(local_8 + 0x14),0,*(size_t *)(local_8 + 0xc));
    FUN__text__0040dc80();
  }
  local_8 = 0x40dc70;
  FUN__text__0056ce80();
  return;
}

