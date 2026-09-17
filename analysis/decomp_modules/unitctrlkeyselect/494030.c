
void __thiscall FUN__text__00494030(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(int *)(param_1 + 0x108b50) != 0) && (*(int *)(param_1 + 0x108b54) == 1)) {
    local_8 = param_1;
    for (local_c = 0; local_c != 10; local_c = local_c + 1) {
      FUN__text__004941a0(local_c);
    }
    FUN__text__004940b0(param_2);
  }
  local_8 = 0x4940a8;
  FUN__text__0056ce80();
  return;
}

