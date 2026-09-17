
void FUN__text__0042abc0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [10];
  undefined4 uStack_24;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*DAT_005921ec)(param_1,0x80000000,1,0,3,1,0);
  local_8 = FUN__text__0056ce80();
  if (local_8 != -1) {
    (*DAT_005921f0)(local_8,0);
    local_c = FUN__text__0056ce80();
    (*DAT_00592270)(local_8);
    FUN__text__0056ce80();
  }
  uStack_24 = 0x42ac4c;
  FUN__text__0056ce80();
  return;
}

