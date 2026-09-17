
void FUN__text__00429b40(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined1 local_14;
  undefined1 local_13;
  undefined1 local_10;
  undefined1 local_f;
  undefined1 local_e;
  undefined1 local_d;
  undefined4 local_c;
  undefined1 local_8;
  undefined1 local_7;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0x5c;
  local_f = 0x2f;
  local_e = 0x3a;
  local_d = 0x2a;
  local_c = 0x3e3c223f;
  local_8 = 0x7c;
  local_7 = 0;
  local_14 = 0x2e;
  local_13 = 0;
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_18 = FUN__text__0056ce80();
  if ((local_18 != 0) && (local_18 < 0x105)) {
    FUN__text__00429990(param_1,&local_10,&local_14);
  }
  local_c = 0x429bd6;
  FUN__text__0056ce80();
  return;
}

