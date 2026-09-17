
void FUN__text1__0080fcfd(int param_1,int param_2)

{
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_10 = 0;
  local_14 = 1;
  local_c = 0;
  local_8 = *(uint *)(param_1 + param_2 * 4);
  if (local_8 == 0xffffffff) {
    local_8 = *(uint *)(param_1 + 0x404);
  }
  for (; local_8 != 0; local_8 = *(uint *)(param_1 + 0x410 + local_8 * 0x10)) {
    if ((local_8 & 1) == 0) {
      local_10 = local_10 | local_14;
    }
    local_14 = local_14 << 1;
    local_c = local_c + 1;
  }
  FUN__text1__00810714(local_10,local_c);
  if (*(int *)(param_1 + param_2 * 4) == -1) {
    FUN__text1__00810714(param_2,8);
    FUN__text1__0081029b(param_1,param_2);
  }
  return;
}

