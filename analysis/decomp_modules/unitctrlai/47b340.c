
/* WARNING: Removing unreachable block (ram,0x0047b4e9) */
/* WARNING: Removing unreachable block (ram,0x0047b57d) */
/* WARNING: Removing unreachable block (ram,0x0047b58b) */
/* WARNING: Removing unreachable block (ram,0x0047b4f7) */

void FUN__text__0047b340(int param_1,undefined4 param_2,int param_3,int param_4,int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_84 [16];
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  char local_34;
  char local_30;
  int local_2c;
  int local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  undefined4 local_14;
  undefined4 local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_84;
  for (iVar1 = 0x20; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  local_10 = FUN__text__0047a8e0(param_1);
  local_20 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                          (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_24 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_38 = 0;
  local_c = (int *)(local_8 + 0xdc8ec);
  local_28 = 0;
  do {
    if (local_28 == *local_c) {
      local_8 = 0x47b758;
      FUN__text__0056ce80();
      return;
    }
    if (*(short *)(param_1 + 2) == *(short *)(local_c[local_28 + 1] + 2)) goto LAB__text__0047b3c3;
    local_34 = '\0';
    local_3c = FUN__text__0046af50(param_1,local_c[local_28 + 1]);
    switch(local_3c) {
    case 0:
      if (param_3 == local_3c) {
        local_34 = '\x01';
      }
      break;
    case 1:
      if (param_3 == local_3c) {
        local_34 = '\x01';
      }
      break;
    case 2:
      if (param_3 == local_3c) {
        local_34 = '\x01';
      }
      break;
    case 3:
      if (param_3 == local_3c) {
        local_34 = '\x01';
      }
      break;
    case 4:
      if (param_3 == local_3c) {
        local_34 = '\x01';
      }
    }
    local_2c = local_3c;
    if (local_34 == '\0') goto LAB__text__0047b3c3;
    local_40 = param_5;
    if ((param_5 == 0) &&
       (*(char *)(*(int *)(param_1 + 600) + 0x98) !=
        *(char *)(*(int *)(local_c[local_28 + 1] + 600) + 0x98))) goto LAB__text__0047b3c3;
    local_44 = param_4 + -1;
    switch(local_44) {
    case 0:
      local_30 = '\x0f';
      local_18 = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_1c = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,0xf);
      break;
    case 1:
      local_30 = '\x1e';
      local_18 = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_1c = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,0x1e);
      goto joined_r0x0047b6fd;
    case 2:
      local_30 = FUN__text__004ddbb0(param_1);
      local_18 = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_1c = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,
                                  (int)local_30);
      break;
    case 3:
      local_30 = FUN__text__004ddbb0(param_1);
      local_18 = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_1c = (short)((int)((*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x10) +
                              (*(int *)(local_c[local_28 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      iVar1 = FUN__text__0043c1d0((int)local_20,(int)local_24,(int)local_18,(int)local_1c,
                                  (int)local_30);
joined_r0x0047b6fd:
      if (iVar1 == 0) goto switchD__text__0047b4d5_default;
      goto LAB__text__0047b3c3;
    default:
      goto switchD__text__0047b4d5_default;
    }
    if (iVar1 != 0) {
switchD__text__0047b4d5_default:
      iVar1 = FUN__text__004690a0(local_c[local_28 + 1]);
      if (iVar1 == 0) {
        FUN__text__00492e20(local_c[local_28 + 1],param_2);
        local_38 = local_38 + 1;
      }
    }
LAB__text__0047b3c3:
    local_28 = local_28 + 1;
  } while( true );
}

