
void FUN__text__0044f1e0(int param_1,int param_2)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  int local_3c;
  int local_38;
  int local_34;
  ushort local_30;
  ushort local_2c;
  ushort local_28;
  ushort local_24;
  undefined1 local_20;
  undefined1 local_1c;
  undefined1 local_18;
  undefined1 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_7c;
  for (iVar1 = 0x1e; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = *(undefined1 *)(param_2 + 0x22);
  local_18 = *(undefined1 *)(param_2 + 0x23);
  local_1c = *(undefined1 *)(param_2 + 0x18);
  local_20 = *(undefined1 *)(param_2 + 0x1a);
  local_c = 1;
  local_10 = param_1;
  DAT_007a3fa4 = local_1c;
  DAT_007a3fa5 = local_20;
  do {
    (&DAT_007a3fa4)[local_c * 2] = *(undefined1 *)(local_10 + 2);
    (&DAT_007a3fa5)[local_c * 2] = *(undefined1 *)(local_10 + 4);
    if (0x62 < local_c) goto LAB__text__0044f2bb;
    local_c = local_c + 1;
    local_10 = *(int *)(local_10 + 0x14);
  } while (local_10 != 0);
  (&DAT_007a3fa4)[local_c * 2] = local_14;
  (&DAT_007a3fa5)[local_c * 2] = local_18;
LAB__text__0044f2bb:
  *(undefined2 *)(param_2 + 0x1e) = 0;
  *(undefined2 *)(param_2 + 0x20) = 0;
  local_3c = local_c;
  local_38 = local_c;
  local_24 = (ushort)(byte)(&DAT_007a3fa4)[local_c * 2];
  local_28 = (ushort)(byte)(&DAT_007a3fa5)[local_c * 2];
  local_34 = 0;
  while( true ) {
    do {
      while( true ) {
        local_2c = (ushort)(byte)(&DAT_007a3fa4)[local_34 * 2];
        uVar2 = (undefined2)((uint)local_34 >> 0x10);
        local_30 = (ushort)(byte)(&DAT_007a3fa5)[local_34 * 2];
        iVar1 = FUN__text__0044f680(local_24,CONCAT22(uVar2,local_28),CONCAT22(uVar2,local_2c),
                                    local_30,0);
        if (iVar1 == 0) break;
        *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) = (undefined1)local_2c;
        *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) = (undefined1)local_30;
        *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
        local_24 = local_2c;
        local_28 = local_30;
        if (local_34 == 0) goto LAB__text__0044f43b;
        local_38 = local_34;
        local_34 = 0;
      }
      local_34 = local_34 + 1;
    } while (local_34 != local_38);
    if (local_38 != local_3c) {
      *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) = (undefined1)local_24;
      *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) = (undefined1)local_28;
      *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
    }
    if (local_34 == 0) break;
    local_38 = local_38 + -1;
    local_24 = (ushort)(byte)(&DAT_007a3fa4)[local_38 * 2];
    local_28 = (ushort)(byte)(&DAT_007a3fa5)[local_38 * 2];
    local_34 = 0;
  }
LAB__text__0044f43b:
  local_8 = 0x44f44f;
  FUN__text__0056ce80();
  return;
}

