
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__0057ef50(uint param_1,uint param_2,int *param_3)

{
  double dVar1;
  int iVar2;
  float10 fVar3;
  double local_10;
  int local_8;
  
  if ((double)CONCAT26(param_2._2_2_,CONCAT24((ushort)param_2,param_1)) == _DAT_00592d98) {
    local_10 = 0.0;
    local_8 = 0;
  }
  else if (((param_2 & 0x7ff00000) == 0) && (((param_2 & 0xfffff) != 0 || (param_1 != 0)))) {
    local_8 = -0x3fd;
    dVar1 = (double)CONCAT26(param_2._2_2_,CONCAT24((ushort)param_2,param_1));
    while ((param_2._2_2_ & 0x10) == 0) {
      iVar2 = CONCAT22(param_2._2_2_,(ushort)param_2) << 1;
      param_2._0_2_ = (ushort)iVar2;
      param_2._2_2_ = (ushort)((uint)iVar2 >> 0x10);
      if ((param_1 & 0x80000000) != 0) {
        param_2._0_2_ = (ushort)param_2 | 1;
      }
      param_1 = param_1 << 1;
      local_8 = local_8 + -1;
    }
    param_2._2_2_ = param_2._2_2_ & 0xffef;
    if (dVar1 < _DAT_00592d98) {
      param_2._2_2_ = param_2._2_2_ | 0x8000;
    }
    fVar3 = (float10)FUN__text__0057ede0(param_1,CONCAT22(param_2._2_2_,(ushort)param_2),0);
    local_10 = (double)fVar3;
  }
  else {
    fVar3 = (float10)FUN__text__0057ede0(param_1,param_2,0);
    local_10 = (double)fVar3;
    local_8 = (short)((int)(param_2._2_2_ & 0x7ff0) >> 4) + -0x3fe;
  }
  *param_3 = local_8;
  return (float10)local_10;
}

