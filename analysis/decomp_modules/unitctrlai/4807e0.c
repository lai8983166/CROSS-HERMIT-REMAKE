
void FUN__text__004807e0(int param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4,
                        int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  short local_20 [2];
  short local_1c [2];
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = FUN__text__00480740(param_1);
  if (param_5 < local_14) {
    local_14 = param_5;
  }
  FUN__text__0043d4e0();
  local_18 = 0;
  local_c = (int *)(local_8 + 0xdccd8);
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    if ((((*(short *)(param_1 + 2) != *(short *)(local_c[local_10 + 1] + 2)) &&
         (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4) ==
          *(char *)(*(int *)(param_1 + 600) + 0xa4))) &&
        (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0x98) ==
         *(char *)(*(int *)(param_1 + 600) + 0x98))) &&
       (((iVar1 = FUN__text__00468d10(local_c[local_10 + 1]), iVar1 != 0 &&
         (iVar1 = FUN__text__0046a120(local_c[local_10 + 1]), iVar1 != 0)) &&
        (iVar1 = FUN__text__0043d660(param_2,CONCAT22((short)((uint)*(int *)(local_c[local_10 + 1] +
                                                                            600) >> 0x10),param_3),
                                     param_4,*(undefined1 *)
                                              (*(int *)(local_c[local_10 + 1] + 600) + 0x30),
                                     local_1c,local_20), iVar1 != 0)))) {
      FUN__text__00480040(0,local_c[local_10 + 1],(int)local_1c[0],(int)local_20[0]);
      local_18 = local_18 + 1;
      if (local_14 <= local_18) break;
    }
  }
  local_8 = 0x480991;
  FUN__text__0056ce80();
  return;
}

