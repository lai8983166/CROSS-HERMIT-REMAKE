
void FUN__text1__0080e2a6(int param_1,uint *param_2,uint *param_3)

{
  void *pvVar1;
  uint local_10;
  uint local_c;
  uint *local_8;
  
  pvVar1 = operator_new(*param_3 << 2);
  FUN__text1__0080fa7d(param_1,*param_3,pvVar1);
  local_10 = 0xffffffff;
  local_8 = param_2 + 1;
  for (local_c = 0; local_c < *param_3; local_c = local_c + 1) {
    if ((local_10 == 0xffffffff) && (*(int *)((int)pvVar1 + local_c * 4) == param_1 + 1)) {
      local_10 = local_c;
    }
    if (*(int *)((int)pvVar1 + local_c * 4) == param_1) {
      *(undefined1 *)local_8 = *(undefined1 *)(param_1 + -1 + *param_3);
    }
    else {
      *(undefined1 *)local_8 = *(undefined1 *)(*(int *)((int)pvVar1 + local_c * 4) + -1);
    }
    local_8 = (uint *)((int)local_8 + 1);
  }
  *param_2 = local_10;
  *param_3 = *param_3 + 4;
  FUN__text1__00848476(pvVar1);
  return;
}

