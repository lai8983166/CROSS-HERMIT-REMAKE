
void FUN__text1__0080fdb3(int param_1,int param_2)

{
  int local_c;
  int local_8;
  
  if (*(int *)(param_1 + 0x40c) == 0x8000) {
    FUN__text1__0080fe8d(param_1);
  }
  for (local_c = *(int *)(param_1 + param_2 * 4); local_c != -1;
      local_c = *(int *)(param_1 + 0x410 + local_c * 0x10)) {
    *(int *)(param_1 + 0x40c + local_c * 0x10) = *(int *)(param_1 + 0x40c + local_c * 0x10) + 1;
    local_8 = local_c;
    while ((0 < local_8 &&
           (*(uint *)(param_1 + 0x40c + (local_8 + -1) * 0x10) <
            *(uint *)(param_1 + 0x40c + local_c * 0x10)))) {
      local_8 = local_8 + -1;
    }
    if (local_c != local_8) {
      FUN__text1__00810105(param_1,local_c,local_8);
      local_c = local_8;
    }
  }
  return;
}

