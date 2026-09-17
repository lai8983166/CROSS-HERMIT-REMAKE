
void FUN__text__00429be0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  undefined1 local_10;
  undefined1 local_f;
  undefined4 local_c;
  undefined1 local_8;
  undefined1 local_7;
  undefined1 local_6;
  undefined1 local_5;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0x223f2a2f;
  local_8 = 0x3c;
  local_7 = 0x3e;
  local_6 = 0x7c;
  local_5 = 0;
  local_10 = 0x2e;
  local_f = 0;
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_14 = FUN__text__0056ce80();
  if ((local_14 != 0) && (local_14 < 4)) {
    FUN__text__00429990(param_1,&local_c,&local_10);
  }
  local_c = 0x429c6b;
  FUN__text__0056ce80();
  return;
}

