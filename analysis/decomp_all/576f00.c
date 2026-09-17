
int * FUN__text__00576f00(int param_1,int *param_2)

{
  int *local_8;
  
  local_8 = param_2;
  do {
    if (*local_8 == param_1) break;
    local_8 = local_8 + 3;
  } while (local_8 < param_2 + DAT_00761dec * 3);
  if ((param_2 + DAT_00761dec * 3 <= local_8) || (*local_8 != param_1)) {
    local_8 = (int *)0x0;
  }
  return local_8;
}

