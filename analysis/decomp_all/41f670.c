
void __thiscall FUN__text__0041f670(int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int *)(param_1 + param_3 * 8);
  local_10 = *local_c;
  local_18 = 0;
  if ((local_c[1] != 0) && (local_10 != 0)) {
    local_8 = param_1;
    for (local_14 = 0; local_14 != local_c[1]; local_14 = local_14 + 1) {
      iVar1 = FUN__text__00405130(param_2,1);
      if (iVar1 != 0) {
        local_18 = local_18 + 1;
      }
    }
  }
  local_8 = 0x41f709;
  FUN__text__0056ce80();
  return;
}

