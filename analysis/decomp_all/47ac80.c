
void FUN__text__0047ac80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_78 [16];
  int local_38;
  int local_34;
  char local_30;
  int local_2c;
  int local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  int local_14;
  int *local_10;
  undefined *local_c;
  int local_8;
  
  puVar2 = local_78;
  for (iVar1 = 0x1d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  local_2c = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40
                            );
  iVar1 = FUN__text__0046c9f0(local_2c);
  if ((((iVar1 != 0) &&
       (local_c = &DAT_006c2dc8 + local_2c * 0x48, *(short *)(&DAT_006c2dca + local_2c * 0x48) == 5)
       ) && (iVar1 = FUN__text__0046c930(param_1,local_2c), iVar1 != 0)) &&
     (iVar1 = FUN__text__00469a30(param_1), iVar1 == 0)) {
    local_20 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                            (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_24 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                            (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    local_30 = FUN__text__004ddc60(param_1,local_2c);
    local_14 = 0;
    local_38 = 100;
    local_10 = (int *)(local_8 + 0xdc8ec);
    for (local_28 = 0; local_28 != *local_10; local_28 = local_28 + 1) {
      iVar1 = FUN__text__0046abc0(param_1,local_10[local_28 + 1]);
      if (((iVar1 != 0) || (iVar1 = FUN__text__0046ad60(param_1,local_10[local_28 + 1]), iVar1 != 0)
          ) && (local_34 = (*(short *)(*(int *)(local_10[local_28 + 1] + 600) + 0x16) * 100) /
                           (int)*(short *)(*(int *)(local_10[local_28 + 1] + 600) + 0x14),
               local_34 < 0x5b)) {
        local_18 = (short)((int)((*(int *)(local_10[local_28 + 1] + 0x2ec) >> 0x10) +
                                (*(int *)(local_10[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
        local_1c = (short)((int)((*(int *)(local_10[local_28 + 1] + 0x2f0) >> 0x10) +
                                (*(int *)(local_10[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
        iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,
                                    (int)local_30);
        if ((iVar1 != 0) && (local_34 < local_38)) {
          local_38 = local_34;
          local_14 = local_10[local_28 + 1];
        }
      }
    }
  }
  local_8 = 0x47aebb;
  FUN__text__0056ce80();
  return;
}

