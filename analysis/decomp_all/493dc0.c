
void __fastcall FUN__text__00493dc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 10; local_10 = local_10 + 1) {
    local_c = (undefined1 *)(local_8 + 0x116098 + local_10 * 0x2c);
    *local_c = 0;
    FUN__text__00427650(0x14);
    for (local_14 = 0; local_14 != 0x14; local_14 = local_14 + 1) {
      FUN__text__00427890(local_14,0);
    }
  }
  local_8 = 0x493e55;
  FUN__text__0056ce80();
  return;
}

