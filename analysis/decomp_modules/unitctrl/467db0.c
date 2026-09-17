
void __fastcall FUN__text__00467db0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x2e70c) = 0x87654321;
  *(undefined4 *)(param_1 + 0x2e710) = 0;
  local_8 = param_1;
  FUN__text__00467d50();
  local_8 = 0x467dfc;
  FUN__text__0056ce80();
  return;
}

