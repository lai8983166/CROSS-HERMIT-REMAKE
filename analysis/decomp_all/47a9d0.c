
void FUN__text__0047a9d0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_78 [16];
  int local_38;
  char local_34;
  char local_30;
  int local_2c;
  int local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_78;
  for (iVar1 = 0x1d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  local_10 = FUN__text__0047a8e0(param_1);
  local_34 = *(char *)(local_10 + 0x10);
  if (local_34 != '\0') {
    if (local_34 != '\x01') goto LAB__text__0047ac61;
    local_20 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                            (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_24 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                            (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    local_30 = FUN__text__004ddbb0(param_1);
  }
  local_c = (int *)(local_8 + 0xdc8ec);
  for (local_28 = 0; local_28 != *local_c; local_28 = local_28 + 1) {
    if (*(short *)(param_1 + 2) != *(short *)(local_c[local_28 + 1] + 2)) {
      iVar1 = FUN__text__00469a30(param_1);
      if ((iVar1 == 0) ||
         (iVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e34 + 0x1c), iVar1 % 100 < 0x33)) {
        iVar1 = FUN__text__0046ac90(param_1,local_c[local_28 + 1]);
        if ((iVar1 == 0) || (iVar1 = FUN__text__0046ae20(param_1,local_c[local_28 + 1]), iVar1 == 0)
           ) {
          local_38 = 0;
        }
        else {
          local_38 = 1;
        }
        local_2c = local_38;
      }
      else {
        local_2c = 1;
      }
      if ((((local_2c != 0) && (iVar1 = FUN__text__004690a0(local_c[local_28 + 1]), iVar1 == 0)) &&
          ((iVar1 = FUN__text__00469ad0(local_c[local_28 + 1]), iVar1 == 0 ||
           (*(char *)(local_10 + 0x1c) != '\0')))) &&
         (iVar1 = FUN__text__0046a050(local_c[local_28 + 1]), iVar1 == 0)) {
        if (*(char *)(local_10 + 0x10) == '\x01') {
          local_18 = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x10) +
                                  (*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
          local_1c = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x10) +
                                  (*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
          iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,
                                      (int)local_30);
          if (iVar1 == 0) goto LAB__text__0047aa72;
        }
        iVar1 = FUN__text__0047aed0(param_1,local_14,local_c[local_28 + 1],
                                    (int)*(char *)(local_10 + 0x11));
        if (iVar1 != 0) {
          local_14 = local_c[local_28 + 1];
        }
      }
    }
LAB__text__0047aa72:
  }
LAB__text__0047ac61:
  local_8 = 0x47ac6e;
  FUN__text__0056ce80();
  return;
}

