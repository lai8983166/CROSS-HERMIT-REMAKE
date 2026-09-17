
void FUN__text1__00810f84(int param_1,uint *param_2,uint *param_3)

{
  uint uVar1;
  undefined2 local_14;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = *param_2;
  local_c = *param_3;
  for (local_14 = 0x11; 1 < local_14; local_14 = local_14 + -1) {
    uVar1 = local_8 ^ *(uint *)(param_1 + 0x1000 + local_14 * 4);
    local_8 = FUN__text1__00810e63(param_1,uVar1);
    local_8 = local_8 ^ local_c;
    local_c = uVar1;
  }
  uVar1 = *(uint *)(param_1 + 0x1004);
  *param_2 = local_c ^ *(uint *)(param_1 + 0x1000);
  *param_3 = local_8 ^ uVar1;
  return;
}

