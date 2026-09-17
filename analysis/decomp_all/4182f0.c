
void FUN__text__004182f0(undefined4 param_1,undefined4 param_2,int param_3,int *param_4,
                        undefined4 param_5,int *param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int *local_c;
  int *local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_6;
  if (*param_6 < 10) {
    local_c = param_6 + *param_6 * 5 + 2;
    local_10 = FUN__text__00428a40(param_3 + 2);
    *local_c = local_10;
    if (*local_c == 0) {
      local_8[1] = local_8[1] + 1;
    }
    else {
      _memset((void *)*local_c,0,param_3 + 2);
      FUN__text__0056d4d0(*local_c,param_2,param_3);
      local_c[1] = *param_4;
      local_c[2] = param_4[1];
      local_c[3] = param_4[2];
      local_c[4] = param_4[3];
      *local_8 = *local_8 + 1;
    }
  }
  local_8 = (int *)0x4183cf;
  FUN__text__0056ce80();
  return;
}

