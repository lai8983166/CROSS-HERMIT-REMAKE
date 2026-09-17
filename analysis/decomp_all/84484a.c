
void FUN__text1__0084484a(int param_1)

{
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_c = 0;
  local_8 = 0;
  for (local_10 = 0; local_10 < 7; local_10 = local_10 + 1) {
    local_8 = local_8 + *(ushort *)(param_1 + 0x8c + local_10 * 4);
  }
  for (; local_10 < 0x80; local_10 = local_10 + 1) {
    local_c = local_c + *(ushort *)(param_1 + 0x8c + local_10 * 4);
  }
  for (; local_10 < 0x100; local_10 = local_10 + 1) {
    local_8 = local_8 + *(ushort *)(param_1 + 0x8c + local_10 * 4);
  }
  *(char *)(param_1 + 0x1c) = '\x01' - (local_c >> 2 < local_8);
  return;
}

