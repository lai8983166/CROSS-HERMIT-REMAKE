
void __thiscall
FUN__text__00489a60(undefined4 param_1,int param_2,int param_3,int *param_4,undefined4 param_5,
                   undefined4 param_6,int param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  char local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*param_4 != 0) && (*param_4 != 1)) &&
      (local_20 = *(char *)(param_7 + 0xe), '\0' < local_20)) && (local_20 < '\x03')) {
    local_8 = param_1;
    for (local_c = 0; iVar1 = local_c, local_c != *param_4 + -1; local_c = local_c + 1) {
      while (local_10 = iVar1 + 1, local_10 != *param_4) {
        iVar1 = FUN__text__0056db00(param_2 - ((int)((*(int *)(param_4[local_c + 1] + 0x2ec) >> 0x10
                                                     ) + (*(int *)(param_4[local_c + 1] + 0x2ec) >>
                                                          0x1f & 0x1fU)) >> 5));
        local_14 = FUN__text__0056db00(param_3 - ((int)((*(int *)(param_4[local_c + 1] + 0x2f0) >>
                                                        0x10) + (*(int *)(param_4[local_c + 1] +
                                                                         0x2f0) >> 0x1f & 0xfU)) >>
                                                 4));
        local_14 = iVar1 + local_14;
        iVar1 = FUN__text__0056db00(param_2 - ((int)((*(int *)(param_4[local_10 + 1] + 0x2ec) >>
                                                     0x10) + (*(int *)(param_4[local_10 + 1] + 0x2ec
                                                                      ) >> 0x1f & 0x1fU)) >> 5));
        local_18 = FUN__text__0056db00(param_3 - ((int)((*(int *)(param_4[local_10 + 1] + 0x2f0) >>
                                                        0x10) + (*(int *)(param_4[local_10 + 1] +
                                                                         0x2f0) >> 0x1f & 0xfU)) >>
                                                 4));
        local_18 = iVar1 + local_18;
        iVar1 = local_10;
        if (local_18 < local_14) {
          local_1c = param_4[local_10 + 1];
          param_4[local_10 + 1] = param_4[local_c + 1];
          param_4[local_c + 1] = local_1c;
        }
      }
    }
  }
  local_8 = 0x489de2;
  FUN__text__0056ce80();
  return;
}

