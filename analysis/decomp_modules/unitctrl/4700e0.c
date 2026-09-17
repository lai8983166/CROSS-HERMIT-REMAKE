
undefined4 FUN__text__004700e0(int param_1,short *param_2,short *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [17];
  short local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_10;
  short local_c;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
  local_10 = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
  local_1c = *(short *)(param_1 + 0x4d0) - local_c;
  local_20 = *(short *)(param_1 + 0x4d2) - local_10;
  if (local_1c < 0) {
    local_24 = -1;
    local_1c = -local_1c;
  }
  else {
    local_24 = 1;
  }
  if (local_20 < 0) {
    local_28 = -1;
    local_20 = -local_20;
  }
  else {
    local_28 = 1;
  }
  if (local_1c < local_20) {
    local_10 = local_10 + local_28;
    if (local_20 <= local_1c) {
      local_c = local_c + local_24;
    }
  }
  else {
    local_c = local_c + local_24;
    if (local_1c <= local_20) {
      local_10 = local_10 + local_28;
    }
  }
  *param_2 = local_c;
  *param_3 = local_10;
  return 0;
}

