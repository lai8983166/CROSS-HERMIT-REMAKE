
void FUN__text__0058dc20(undefined2 *param_1,uint param_2,int param_3)

{
  uint uVar1;
  undefined2 local_18;
  undefined4 uStack_16;
  undefined2 uStack_12;
  undefined *local_10;
  undefined **local_c;
  undefined **local_8;
  
  local_8 = &PTR_DAT_00765200;
  if (param_2 != 0) {
    if ((int)param_2 < 0) {
      param_2 = -param_2;
      local_8 = (undefined **)&DAT_00765360;
    }
    uStack_16 = CONCAT22(uStack_16._2_2_,(undefined2)uStack_16);
    if (param_3 == 0) {
      *param_1 = 0;
      uStack_16 = CONCAT22(uStack_16._2_2_,(undefined2)uStack_16);
    }
    while (param_2 != 0) {
      local_8 = local_8 + 0x15;
      uVar1 = param_2 & 7;
      param_2 = (int)param_2 >> 3;
      if (uVar1 != 0) {
        local_c = local_8 + uVar1 * 3;
        if (0x7fff < *(ushort *)local_c) {
          local_18 = SUB42(*local_c,0);
          uStack_16._0_2_ = (undefined2)((uint)*local_c >> 0x10);
          uStack_16._2_2_ = SUB42(local_c[1],0);
          uStack_12 = (undefined2)((uint)local_c[1] >> 0x10);
          local_10 = local_c[2];
          uStack_16 = CONCAT22(uStack_16._2_2_,(undefined2)uStack_16) + -1;
          local_c = (undefined **)&local_18;
        }
        FUN__text__0058d7e0(param_1,local_c);
      }
    }
  }
  return;
}

