
void FUN__text__0047fc60(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        )

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
  FUN__text__0043d4e0();
  local_10 = 0;
  for (local_c = 4; local_c != 0x10; local_c = local_c + 1) {
    iVar1 = FUN__text__0047fe70(0,local_c,param_1,param_2,param_3,param_4);
    local_10 = local_10 + iVar1;
  }
  local_8 = 0x47fce2;
  FUN__text__0056ce80();
  return;
}

