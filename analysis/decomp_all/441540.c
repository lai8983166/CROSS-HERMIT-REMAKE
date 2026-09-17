
void FUN__text__00441540(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
    FUN__text__004077c0(param_1);
    FUN__text__00409480(*local_8);
    FUN__text__004094c0(1);
  }
  local_8 = (undefined4 *)0x4415da;
  FUN__text__0056ce80();
  return;
}

