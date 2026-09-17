
void FUN__text__004212e0(int param_1,int param_2,int *param_3,int *param_4)

{
  byte bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  byte local_34;
  undefined3 uStack_33;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(short *)(param_1 + 0x1c) == 8) {
    local_c = *(int *)(param_1 + 0x12);
    local_10 = *(int *)(param_1 + 0x16);
    local_14 = FUN__text__00420ac0(param_1);
    local_1c = FUN__text__00420b00(param_1);
    local_18 = param_2 + 0xc;
    for (local_2c = 0; local_2c != param_3[3]; local_2c = local_2c + 1) {
      local_20 = local_14 + *param_3 + ((local_10 - (param_3[1] + local_2c)) + -1) * local_c;
      local_24 = local_18 + *param_4 * 2 +
                 (param_4[1] + local_2c) * 2 * (uint)*(ushort *)(param_2 + 8);
      if ((int)(uint)*(ushort *)(param_2 + 4) < param_3[2]) {
        local_30 = (uint)*(ushort *)(param_2 + 4) - *param_4;
      }
      else {
        local_30 = param_3[2];
      }
      for (local_28 = 0; local_28 != local_30; local_28 = local_28 + 1) {
        bVar1 = *(byte *)(local_20 + local_28);
        _local_34 = CONCAT31(uStack_33,bVar1);
        if (bVar1 == 0) {
          *(undefined2 *)(local_24 + local_28 * 2) = 0;
        }
        else if (((*(char *)(local_1c + 2 + (uint)bVar1 * 4) == '\0') &&
                 (*(char *)(local_1c + 1 + (uint)bVar1 * 4) == '\0')) &&
                (*(char *)(local_1c + (uint)bVar1 * 4) == '\0')) {
          *(undefined2 *)(local_24 + local_28 * 2) = 0;
        }
        else {
          *(ushort *)(local_24 + local_28 * 2) =
               (ushort)(((int)(uint)*(byte *)(local_1c + 2 + (uint)bVar1 * 4) >> 3) << 10) |
               (ushort)(((int)(uint)*(byte *)(local_1c + 1 + (uint)bVar1 * 4) >> 3) << 5) |
               (ushort)((int)(uint)*(byte *)(local_1c + (uint)bVar1 * 4) >> 3) | 0x8000;
        }
      }
    }
  }
  local_8 = 0x4214e9;
  FUN__text__0056ce80();
  return;
}

