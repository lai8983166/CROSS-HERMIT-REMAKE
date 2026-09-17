
void FUN__text__004210d0(int param_1,int param_2,int *param_3,int *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_70 [16];
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
  
  puVar2 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 0x1c) == 8) {
    local_c = *(int *)(param_1 + 0x12);
    local_10 = *(int *)(param_1 + 0x16);
    local_14 = FUN__text__00420ac0(param_1);
    local_1c = FUN__text__00420b00(param_1);
    if ((*(ushort *)(param_2 + 2) & 0x8000) == 0) {
      local_18 = param_2 + 0xc;
    }
    else {
      FUN__text__00420a40(param_1);
      for (local_20 = 0; local_20 != *(int *)(param_1 + 0x2e); local_20 = local_20 + 1) {
        if ((local_20 == 0) ||
           (((*(char *)(local_1c + local_20 * 4) == '\0' &&
             (*(char *)(local_1c + 1 + local_20 * 4) == '\0')) &&
            (*(char *)(local_1c + 2 + local_20 * 4) == '\0')))) {
          *(undefined4 *)(param_2 + 0xc + local_20 * 4) = 0;
        }
        else {
          *(undefined1 *)(param_2 + 0xc + local_20 * 4) = 0;
          *(undefined1 *)(param_2 + 0xf + local_20 * 4) =
               *(undefined1 *)(local_1c + 2 + local_20 * 4);
          *(undefined1 *)(param_2 + 0xe + local_20 * 4) =
               *(undefined1 *)(local_1c + 1 + local_20 * 4);
          *(undefined1 *)(param_2 + 0xd + local_20 * 4) = *(undefined1 *)(local_1c + local_20 * 4);
        }
      }
      local_18 = param_2 + 0x40c;
    }
    for (local_2c = 0; local_2c != param_3[3]; local_2c = local_2c + 1) {
      local_24 = local_14 + *param_3 + ((local_10 - (param_3[1] + local_2c)) + -1) * local_c;
      local_28 = local_18 + *param_4 + (param_4[1] + local_2c) * (uint)*(ushort *)(param_2 + 8);
      if ((int)(uint)*(ushort *)(param_2 + 4) < param_3[2]) {
        local_30 = (uint)*(ushort *)(param_2 + 4) - *param_4;
      }
      else {
        local_30 = param_3[2];
      }
      FUN__text__0056d4d0(local_28,local_24,local_30);
    }
  }
  local_8 = 0x4212d8;
  FUN__text__0056ce80();
  return;
}

