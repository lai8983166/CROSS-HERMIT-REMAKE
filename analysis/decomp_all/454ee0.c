
void __fastcall FUN__text__00454ee0(undefined4 param_1)

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
  local_8 = param_1;
  for (local_c = 10; local_c != 0x59; local_c = local_c + 1) {
    local_10 = local_c;
    if (local_c != 0x14) {
      FUN__text__0041f4e0(local_c);
    }
  }
  local_8 = 0x454f49;
  FUN__text__0056ce80();
  return;
}

