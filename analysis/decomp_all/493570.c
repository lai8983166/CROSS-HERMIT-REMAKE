
void FUN__text__00493570(int param_1)

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
  if (*(int *)(param_1 + 0x510) != 0) {
    local_c = *(int *)(param_1 + 0x510);
    while (local_c != 0) {
      local_10 = *(int *)(local_c + 4);
      FUN__text__00492f00(local_c);
      local_c = local_10;
    }
    *(undefined4 *)(param_1 + 0x510) = 0;
  }
  local_8 = 0x4935e2;
  FUN__text__0056ce80();
  return;
}

