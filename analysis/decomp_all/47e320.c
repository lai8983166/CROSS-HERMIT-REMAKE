
void __thiscall FUN__text__0047e320(int param_1,short param_2,short param_3)

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
  local_c = (int *)(param_1 + 0xdc8ec);
  local_8 = param_1;
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    iVar1 = FUN__text__00468d10(local_c[local_10 + 1]);
    if (iVar1 != 0) {
      local_14 = (int)((*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x10) +
                      (*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_18 = (int)((*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x10) +
                      (*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      if ((local_14 == param_2) && (local_18 == param_3)) break;
    }
  }
  local_8 = 0x47e3eb;
  FUN__text__0056ce80();
  return;
}

