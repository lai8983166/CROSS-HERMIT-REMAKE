
void FUN__text__0047f9d0(undefined4 param_1)

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
  local_10 = 0;
  for (local_c = 4; local_c != 0x10; local_c = local_c + 1) {
    iVar1 = FUN__text__0047fa40(0,local_c,param_1);
    local_10 = local_10 + iVar1;
  }
  local_8 = 0x47fa38;
  FUN__text__0056ce80();
  return;
}

