
void __thiscall FUN__text__00416a10(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = 0;
  local_8 = param_1;
  for (local_10 = 0; local_10 != 0x100; local_10 = local_10 + 1) {
    local_14 = FUN__text__0041ef60(local_10);
    for (local_c = 0; local_c != local_14; local_c = local_c + 1) {
      FUN__text__00416af0(param_2,local_10,local_c);
      local_18 = local_18 + 1;
    }
  }
  FUN__text__00410310(0,0,0x400,0x300,0,0xff000000,0);
  FUN__text__0042b2d0(&DAT_00592d70,local_18);
  local_8 = 0x416ae5;
  FUN__text__0056ce80();
  return;
}

