
uint * FUN__text1__00834599(uint *param_1,int param_2,uint *param_3,int param_4)

{
  uint uVar1;
  void *pvVar2;
  bool bVar3;
  uint local_8;
  
  local_8 = *param_1;
  param_1 = param_1 + 1;
  bVar3 = (local_8 & 0x80000000) != 0;
  if (bVar3) {
    local_8 = local_8 & 0x7fffffff;
  }
  uVar1 = local_8;
  if (local_8 != 0) {
    if (param_2 == 0) {
      param_1 = (uint *)((int)param_1 + local_8);
    }
    else {
      if (bVar3) {
        FUN__text1__00848490(param_2,param_1,local_8);
        if (param_4 != 0) {
          FUN__text1__00811f18(param_4,param_2,local_8,0);
        }
      }
      else {
        pvVar2 = operator_new(local_8 + 0x100);
        FUN__text1__00848490(pvVar2,param_1,local_8);
        if (param_4 != 0) {
          FUN__text1__00811f18(param_4,pvVar2,local_8,0);
        }
        local_8 = FUN__text1__0081132e(pvVar2,param_2,local_8,*param_3);
        if (local_8 == 0) {
          DAT_008750d8 = 0;
          return (uint *)0x0;
        }
        FUN__text1__00848476(pvVar2);
      }
      param_1 = (uint *)((int)param_1 + uVar1);
    }
  }
  *param_3 = local_8;
  return param_1;
}

