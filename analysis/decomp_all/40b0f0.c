
void __thiscall
FUN__text__0040b0f0(undefined4 param_1,int param_2,int param_3,int param_4,int param_5,
                   undefined2 param_6,undefined2 param_7,undefined2 param_8)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_78 [16];
  uint local_38;
  undefined1 local_34;
  undefined1 local_33;
  undefined1 local_32;
  ushort local_30;
  undefined2 uStack_2e;
  ushort local_2c;
  undefined2 uStack_2a;
  int local_28;
  int local_24;
  int local_20;
  ushort local_1c [4];
  ushort *local_14;
  short *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_78;
  for (iVar2 = 0x1d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (((*(int *)(param_2 + 0x2c) == 0) || (*(short *)(param_2 + 0x48) < 1)) &&
     (*(int *)(param_2 + 0x28) != 0)) {
    local_c = *(int *)(param_2 + 0x28);
    local_1c[0] = (ushort)*(byte *)(local_c + 2) | (*(ushort *)(local_c + 6) & 0xf) << 8;
    local_1c[1] = (ushort)*(byte *)(local_c + 3) | (*(ushort *)(local_c + 6) & 0xf0) << 4;
    local_1c[2] = (ushort)*(byte *)(local_c + 4) | *(ushort *)(local_c + 6) & 0xf00;
    local_1c[3] = (ushort)*(byte *)(local_c + 5) |
                  (ushort)((int)(*(ushort *)(local_c + 6) & 0xf000) >> 4);
    if ((*(byte *)(param_2 + 3) & 8) != 0) {
      local_34 = *(undefined1 *)(param_3 + 0x66);
      local_33 = *(undefined1 *)(param_3 + 0x65);
      local_32 = *(undefined1 *)(param_3 + 100);
      *(undefined1 *)(param_3 + 0x66) = *(undefined1 *)(param_2 + 0x54);
      *(undefined1 *)(param_3 + 0x65) = *(undefined1 *)(param_2 + 0x55);
      *(undefined1 *)(param_3 + 100) = *(undefined1 *)(param_2 + 0x56);
    }
    for (local_20 = 3; -1 < local_20; local_20 = local_20 + -1) {
      if (local_1c[local_20] < 0xfff) {
        local_10 = (short *)FUN__text__00409fb0(param_2,local_1c[local_20]);
        local_1c[local_20] = local_10[2];
        local_38 = *(byte *)(local_10 + 3) & 3;
        if ((*(byte *)(local_10 + 3) & 3) == 0) {
LAB__text__0040b281:
          *(undefined1 *)(param_3 + 0x67) = 0xff;
          *(undefined4 *)(param_3 + 0x5c) = 0;
        }
        else if (local_38 == 1) {
          if (*(char *)((int)local_10 + 7) == -1) goto LAB__text__0040b281;
          *(undefined1 *)(param_3 + 0x67) = *(undefined1 *)((int)local_10 + 7);
          *(undefined4 *)(param_3 + 0x5c) = 1;
        }
        else if (local_38 == 2) {
          *(undefined1 *)(param_3 + 0x67) = *(undefined1 *)((int)local_10 + 7);
          *(undefined4 *)(param_3 + 0x5c) = 2;
        }
        FUN__text__00407870(*(undefined4 *)(*(int *)(param_2 + 0x1c) + 0x28),local_1c[local_20]);
        local_14 = (ushort *)FUN__text__0041ed00(local_1c[local_20]);
        if ((*(byte *)(param_2 + 3) & 1) == 0) {
          uVar1 = local_14[2];
        }
        else {
          uVar1 = *local_14 - (*(short *)(param_3 + 0x38) + local_14[2]);
        }
        _local_2c = CONCAT22(uStack_2a,uVar1);
        if ((*(byte *)(param_2 + 3) & 2) == 0) {
          uVar3 = local_14[3];
        }
        else {
          uVar3 = local_14[1] - (*(short *)(param_3 + 0x3a) + local_14[3]);
        }
        _local_30 = CONCAT22(uStack_2e,uVar3);
        if ((*(byte *)(param_2 + 3) & 1) == 0) {
          local_24 = (int)*local_10;
        }
        else {
          local_24 = -(int)*local_10;
        }
        local_24 = ((uint)uVar1 - ((int)(uint)*local_14 >> 1)) + (int)*(short *)(param_2 + 0x12) +
                   local_24;
        if ((*(byte *)(param_2 + 3) & 2) == 0) {
          local_28 = ((uint)uVar3 - ((int)(uint)local_14[1] >> 1)) + (int)*(short *)(param_2 + 0x14)
                     + (int)local_10[1];
        }
        else {
          local_28 = -(int)local_10[1];
        }
        if ((char)local_10[4] == '\0') {
          *(undefined2 *)(param_3 + 0x76) = param_7;
        }
        else if (*(byte *)(local_10 + 4) < 0xd) {
          *(undefined2 *)(param_3 + 0x76) = param_6;
        }
        else {
          *(undefined2 *)(param_3 + 0x76) = param_8;
        }
        *(ushort *)(param_3 + 0x58) = *(ushort *)(param_3 + 0x58) & 0xffcf;
        if ((*(byte *)(param_2 + 3) & 1) != 0) {
          *(ushort *)(param_3 + 0x58) = *(ushort *)(param_3 + 0x58) | 0x10;
        }
        if ((*(byte *)(param_2 + 3) & 2) != 0) {
          *(ushort *)(param_3 + 0x58) = *(ushort *)(param_3 + 0x58) | 0x20;
        }
        if (((*(ushort *)(param_3 + 0x58) & 1) != 0) && (*(short *)(param_3 + 0x70) != 100)) {
          local_24 = (*(short *)(param_3 + 0x70) * local_24) / 100;
        }
        if (((*(ushort *)(param_3 + 0x58) & 1) != 0) && (*(short *)(param_3 + 0x72) != 100)) {
          local_28 = (*(short *)(param_3 + 0x72) * local_28) / 100;
        }
        FUN__text__004079c0(param_4 + local_24,param_5 + local_28);
        *(ushort *)(param_3 + 0x58) = *(ushort *)(param_3 + 0x58) & 0xfeff;
      }
    }
    if ((*(byte *)(param_2 + 3) & 8) != 0) {
      *(undefined1 *)(param_3 + 0x66) = local_34;
      *(undefined1 *)(param_3 + 0x65) = local_33;
      *(undefined1 *)(param_3 + 100) = local_32;
    }
  }
  local_8 = 0x40b585;
  FUN__text__0056ce80();
  return;
}

