
void FUN__text__0058b5b0(char *param_1,int param_2,uint *param_3)

{
  short local_14;
  uint local_10;
  uint local_c;
  uint local_8;
  
  local_14 = 0x404e;
  *param_3 = 0;
  param_3[1] = 0;
  param_3[2] = 0;
  for (; param_2 != 0; param_2 = param_2 + -1) {
    local_10 = *param_3;
    local_c = param_3[1];
    local_8 = param_3[2];
    ___shl_12(param_3);
    ___shl_12(param_3);
    ___add_12(param_3,&local_10);
    ___shl_12(param_3);
    local_10 = (uint)*param_1;
    local_c = 0;
    local_8 = 0;
    ___add_12(param_3,&local_10);
    param_1 = param_1 + 1;
  }
  while (param_3[2] == 0) {
    param_3[2] = param_3[1] >> 0x10;
    param_3[1] = param_3[1] << 0x10 | *param_3 >> 0x10;
    *param_3 = *param_3 << 0x10;
    local_14 = local_14 + -0x10;
  }
  while ((param_3[2] & 0x8000) == 0) {
    ___shl_12(param_3);
    local_14 = local_14 + -1;
  }
  *(short *)((int)param_3 + 10) = local_14;
  return;
}

