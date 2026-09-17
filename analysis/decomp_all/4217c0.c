
void __fastcall FUN__text__004217c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 0x20; local_c = local_c + 1) {
    local_18 = *(int *)(local_8 + local_c * 8);
    local_14 = *(undefined4 *)(local_8 + 4 + local_c * 8);
    while (iVar1 = local_18, local_18 != 0) {
      local_10 = local_18;
      local_14 = *(undefined4 *)(local_18 + 0x10);
      local_18 = *(int *)(local_18 + 0xc);
      FUN__text__00421850(iVar1);
    }
  }
  local_8 = 0x421842;
  FUN__text__0056ce80();
  return;
}

