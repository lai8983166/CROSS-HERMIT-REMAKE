
void FUN__text__00405d80(int param_1,int *param_2,int param_3,undefined4 param_4,int *param_5,
                        int *param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  uint local_28;
  uint local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 0x1c) == 8) {
    local_c = FUN__text__00420ac0(param_1);
    local_10 = FUN__text__00420b00(param_1);
    for (local_20 = 0; local_20 != param_5[3]; local_20 = local_20 + 1) {
      local_14 = local_c + *param_5 * 4 + (param_5[1] + local_20) * 4 * param_3;
      local_18 = param_2[1] + *param_6 + (param_6[1] + local_20) * *param_2;
      for (local_1c = 0; local_1c != param_5[2]; local_1c = local_1c + 1) {
        local_24 = *(uint *)(local_14 + local_1c * 4);
        if ((local_24 & 0xffffff) == 0) {
          *(undefined1 *)(local_18 + local_1c) = 0;
        }
        else {
          local_28 = local_24 & 0xffffff;
          if (local_28 == 0xffffff) {
            *(undefined1 *)(local_18 + local_1c) = 1;
          }
          else {
            *(undefined1 *)(local_18 + local_1c) = 2;
          }
        }
      }
    }
  }
  local_8 = 0x405eab;
  FUN__text__0056ce80();
  return;
}

