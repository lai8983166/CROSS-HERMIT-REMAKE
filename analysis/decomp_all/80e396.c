
void FUN__text1__0080e396(char *param_1,char *param_2,int param_3)

{
  char local_118 [256];
  int local_18;
  char *local_14;
  char *local_10;
  char *local_c;
  char *local_8;
  
  for (local_18 = 0; local_18 < 0x100; local_18 = local_18 + 1) {
    local_118[local_18] = (char)local_18;
  }
  local_10 = param_2;
  local_14 = param_1 + param_3;
  for (local_c = param_1; local_c < local_14; local_c = local_c + 1) {
    for (local_8 = local_118; *local_8 != *local_c; local_8 = local_8 + 1) {
    }
    *local_10 = (char)local_8 - (char)local_118;
    local_10 = local_10 + 1;
    if (local_8 != local_118) {
      FUN__text1__008487d0(local_118 + 1,local_118,(int)local_8 - (int)local_118);
      local_118[0] = *local_c;
    }
  }
  return;
}

