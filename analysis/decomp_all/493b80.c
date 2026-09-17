
void __fastcall FUN__text__00493b80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 5; local_c = local_c + 1) {
    if (*(char *)(local_8 + 0x116254 + local_c * 0x524) != '\0') {
      local_18 = local_8 + 0x116258 + local_c * 0x524;
      local_10 = *(int *)(local_18 + 0x2ec) >> 0x10;
      local_14 = *(int *)(local_18 + 0x2f0) >> 0x10;
      FUN__text__0040a330(local_18 + 0x48,local_8 + 0xde4b0,local_10,local_14,0xc4);
    }
  }
  local_8 = 0x493c3c;
  FUN__text__0056ce80();
  return;
}

