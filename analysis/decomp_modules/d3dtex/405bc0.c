
void FUN__text__00405bc0(int param_1,int *param_2,int param_3,int param_4,int *param_5,int *param_6)

{
  ushort uVar1;
  ushort uVar2;
  int iVar3;
  ushort uVar4;
  undefined4 *puVar5;
  undefined4 local_6c [16];
  ushort local_2c;
  undefined2 uStack_2a;
  ushort local_28;
  undefined2 uStack_26;
  ushort local_24;
  undefined2 uStack_22;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar5 = local_6c;
  for (iVar3 = 0x1a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if (*(short *)(param_1 + 0x1c) == 8) {
    local_c = FUN__text__00420ac0(param_1);
    local_10 = FUN__text__00420b00(param_1);
    for (local_20 = 0; local_20 != param_5[3]; local_20 = local_20 + 1) {
      local_14 = local_c + *param_5 + ((param_4 - (param_5[1] + local_20)) + -1) * param_3;
      local_18 = param_2[1] + *param_6 * 2 + (param_6[1] + local_20) * *param_2;
      for (local_1c = 0; local_1c != param_5[2]; local_1c = local_1c + 1) {
        if (*(char *)(local_14 + local_1c) == '\0') {
          *(undefined2 *)(local_18 + local_1c * 2) = 0;
        }
        else {
          uVar1 = (*(byte *)(local_10 + 2 + (uint)*(byte *)(local_14 + local_1c) * 4) & 0xf8) << 7;
          _local_24 = CONCAT22(uStack_22,uVar1);
          uVar2 = (*(byte *)(local_10 + 1 + (uint)*(byte *)(local_14 + local_1c) * 4) & 0xf8) << 2;
          _local_28 = CONCAT22(uStack_26,uVar2);
          uVar4 = (ushort)((int)(*(byte *)(local_10 + (uint)*(byte *)(local_14 + local_1c) * 4) &
                                0xf8) >> 3);
          _local_2c = CONCAT22(uStack_2a,uVar4);
          *(ushort *)(local_18 + local_1c * 2) = uVar1 | 0x8000 | uVar2 | uVar4;
        }
      }
    }
  }
  local_8 = 0x405d7a;
  FUN__text__0056ce80();
  return;
}

