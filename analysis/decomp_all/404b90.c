
void FUN__text__00404b90(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined1 local_10 [4];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0042ae70(param_2,local_10);
  if (local_c != 0) {
    local_14 = FUN__text__00404870(param_1,0,local_c,param_3,param_4,param_5);
    local_18 = local_c;
    FUN__text__00428ad0(local_c);
  }
  local_8 = 0x404c10;
  FUN__text__0056ce80();
  return;
}

