
void FUN__text1__00842d3c(int param_1,int param_2,int param_3)

{
  ushort uVar1;
  uint uVar2;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_1c = 0xffffffff;
  uVar1 = *(ushort *)(param_2 + 2);
  local_8 = 0;
  local_10 = 7;
  local_14 = 4;
  if (uVar1 == 0) {
    local_10 = 0x8a;
    local_14 = 3;
  }
  *(undefined2 *)(param_2 + 6 + param_3 * 4) = 0xffff;
  local_c = (uint)uVar1;
  for (local_20 = 0; local_20 <= param_3; local_20 = local_20 + 1) {
    uVar2 = (uint)*(ushort *)(param_2 + 6 + local_20 * 4);
    local_8 = local_8 + 1;
    if ((local_10 <= local_8) || (local_c != uVar2)) {
      if (local_8 < local_14) {
        *(short *)(param_1 + 0xa74 + local_c * 4) =
             *(short *)(param_1 + 0xa74 + local_c * 4) + (short)local_8;
      }
      else if (local_c == 0) {
        if (local_8 < 0xb) {
          *(short *)(param_1 + 0xab8) = *(short *)(param_1 + 0xab8) + 1;
        }
        else {
          *(short *)(param_1 + 0xabc) = *(short *)(param_1 + 0xabc) + 1;
        }
      }
      else {
        if (local_c != local_1c) {
          *(short *)(param_1 + 0xa74 + local_c * 4) = *(short *)(param_1 + 0xa74 + local_c * 4) + 1;
        }
        *(short *)(param_1 + 0xab4) = *(short *)(param_1 + 0xab4) + 1;
      }
      local_8 = 0;
      local_1c = local_c;
      if (uVar2 == 0) {
        local_10 = 0x8a;
        local_14 = 3;
      }
      else if (local_c == uVar2) {
        local_10 = 6;
        local_14 = 3;
      }
      else {
        local_10 = 7;
        local_14 = 4;
      }
    }
    local_c = uVar2;
  }
  return;
}

