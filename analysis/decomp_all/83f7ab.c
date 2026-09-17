
uint FUN__text1__0083f7ab(int *param_1,undefined4 param_2,uint param_3)

{
  int iVar1;
  uint local_8;
  
  local_8 = param_1[1];
  if (param_3 < local_8) {
    local_8 = param_3;
  }
  if (local_8 == 0) {
    local_8 = 0;
  }
  else {
    param_1[1] = param_1[1] - local_8;
    if (*(int *)(param_1[7] + 0x18) == 0) {
      iVar1 = FUN__text1__00841580(param_1[0xc],*param_1,local_8);
      param_1[0xc] = iVar1;
    }
    FUN__text1__00848490(param_2,*param_1,local_8);
    *param_1 = *param_1 + local_8;
    param_1[2] = param_1[2] + local_8;
  }
  return local_8;
}

