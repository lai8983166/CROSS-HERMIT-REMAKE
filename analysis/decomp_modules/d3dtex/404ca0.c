
void FUN__text__00404ca0(undefined4 param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_8c [16];
  uint local_4c;
  undefined1 local_48 [24];
  undefined2 local_30;
  undefined2 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  uint local_20;
  int local_1c;
  byte *local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_8c;
  for (iVar1 = 0x22; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00403730();
  local_c = param_2;
  iVar1 = FUN__text__004209f0(param_2);
  if (iVar1 == 0) {
    FUN__text__00420a40(local_c);
    local_14 = *(undefined4 *)(local_c + 2);
    local_4c = (uint)*(ushort *)(local_c + 0x1c);
    if (local_4c == 4) {
      local_18 = (byte *)(local_c + 0x36);
      local_20 = (uint)*(byte *)(local_c + 0x38) << 0x10 | 0xff000000 |
                 (uint)*(byte *)(local_c + 0x37) << 8 | (uint)*local_18;
      local_24 = 0x28;
      if (param_4 == 1) {
        for (local_10 = 0; local_10 != *(int *)(local_c + 0x2e); local_10 = local_10 + 1) {
          if ((((*(char *)(local_c + 0x38 + local_10 * 4) == '\0') &&
               (*(char *)(local_c + 0x37 + local_10 * 4) == '\0')) && (local_18[local_10 * 4] == 0))
             && (local_10 != 0)) {
            *(undefined4 *)(local_18 + local_10 * 4) = *(undefined4 *)local_18;
          }
        }
      }
      if (param_3 == 0) {
        local_20 = 0;
      }
    }
    else if (local_4c == 8) {
      local_18 = (byte *)(local_c + 0x36);
      local_20 = (uint)*(byte *)(local_c + 0x38) << 0x10 | 0xff000000 |
                 (uint)*(byte *)(local_c + 0x37) << 8 | (uint)*local_18;
      local_24 = 0x19;
      if (param_4 == 1) {
        for (local_10 = 0; local_10 != *(int *)(local_c + 0x2e); local_10 = local_10 + 1) {
          if (((*(char *)(local_c + 0x38 + local_10 * 4) == '\0') &&
              (*(char *)(local_c + 0x37 + local_10 * 4) == '\0')) &&
             ((local_18[local_10 * 4] == 0 && (local_10 != 0)))) {
            *(undefined4 *)(local_18 + local_10 * 4) = *(undefined4 *)local_18;
          }
        }
      }
      if (param_3 == 0) {
        local_20 = 0;
      }
    }
    else {
      local_20 = 0xff000000;
      if (param_3 == 0) {
        local_20 = 0;
      }
      local_24 = 0;
    }
    *(undefined2 *)(local_8 + 0x38) = *(undefined2 *)(local_c + 0x12);
    *(undefined2 *)(local_8 + 0x3a) = *(undefined2 *)(local_c + 0x16);
    local_1c = FUN__text__0052a01b(param_1,param_2,local_14,(int)*(short *)(local_8 + 0x38),
                                   (int)*(short *)(local_8 + 0x3a),1,0,local_24,1,1,1,local_20,0,0,
                                   local_8 + 0x2c);
    if (-1 < local_1c) {
      (**(code **)(**(int **)(local_8 + 0x2c) + 0x34))(*(undefined4 *)(local_8 + 0x2c));
      local_28 = FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 0x2c) + 0x38))(*(undefined4 *)(local_8 + 0x2c),0,local_48);
      local_1c = FUN__text__0056ce80();
      if (-1 < local_1c) {
        *(undefined2 *)(local_8 + 0x3c) = local_30;
        *(undefined2 *)(local_8 + 0x3e) = local_2c;
      }
      *(undefined4 *)(local_8 + 0x28) = param_1;
    }
  }
  local_8 = 0x404fa4;
  FUN__text__0056ce80();
  return;
}

