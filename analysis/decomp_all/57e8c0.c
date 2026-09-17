
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN__text__0057e8c0(uint param_1,double *param_2,uint param_3)

{
  double dVar1;
  ulonglong uVar2;
  uint uVar3;
  float10 fVar4;
  undefined8 local_44;
  undefined8 local_3c;
  undefined8 local_34;
  undefined8 local_2c;
  int local_1c;
  int local_18;
  undefined8 local_14;
  uint local_c;
  uint local_8;
  
  local_8 = param_1 & 0x1f;
  if (((param_1 & 8) == 0) || ((param_3 & 1) == 0)) {
    if (((param_1 & 4) == 0) || ((param_3 & 4) == 0)) {
      if (((param_1 & 1) == 0) || ((param_3 & 8) == 0)) {
        if (((param_1 & 2) != 0) && ((param_3 & 0x10) != 0)) {
          local_c = (uint)((param_1 & 0x10) != 0);
          if (*param_2 == _DAT_00592d98) {
            local_c = 1;
          }
          else {
            fVar4 = (float10)FUN__text__0057ef50(*(undefined4 *)param_2,
                                                 *(undefined4 *)((int)param_2 + 4),&local_1c);
            dVar1 = (double)fVar4;
            local_18 = local_1c + -0x600;
            if (local_18 < -0x432) {
              local_14 = dVar1 * _DAT_00592d98;
              local_c = 1;
            }
            else {
              local_14 = (double)((ulonglong)dVar1 & 0xfffffffffffff);
              local_14 = (double)((ulonglong)local_14 | 0x10000000000000);
              for (; local_18 < -0x3fd; local_18 = local_18 + 1) {
                if ((((ulonglong)local_14 & 1) != 0) && (local_c == 0)) {
                  local_c = 1;
                }
                uVar3 = (uint)local_14 >> 1;
                uVar2 = (ulonglong)local_14 & 0x100000000;
                local_14._0_4_ = uVar3;
                if (uVar2 != 0) {
                  local_14._0_4_ = uVar3 | 0x80000000;
                }
                local_14 = (double)CONCAT44(local_14._4_4_ >> 1,(uint)local_14);
              }
              if (dVar1 < _DAT_00592d98) {
                local_14 = -local_14;
              }
            }
            *(uint *)param_2 = (uint)local_14;
            *(uint *)((int)param_2 + 4) = local_14._4_4_;
          }
          if (local_c != 0) {
            FUN__text__0057f110(0x10);
          }
          local_8 = local_8 & 0xfffffffd;
        }
      }
      else {
        FUN__text__0057f110(8);
        uVar3 = param_3 & 0xc00;
        if (uVar3 < 0x801) {
          if (uVar3 == 0x800) {
            if (*param_2 <= _DAT_00592d98) {
              local_34 = -(double)CONCAT44(DAT_007646dc,DAT_007646d8);
            }
            else {
              local_34 = (double)CONCAT44(DAT_007646cc,DAT_007646c8);
            }
            *(undefined4 *)param_2 = (undefined4)local_34;
            *(undefined4 *)((int)param_2 + 4) = local_34._4_4_;
          }
          else if (uVar3 == 0) {
            if (*param_2 <= _DAT_00592d98) {
              local_2c = -(double)CONCAT44(DAT_007646cc,DAT_007646c8);
            }
            else {
              local_2c = (double)CONCAT44(DAT_007646cc,DAT_007646c8);
            }
            *(undefined4 *)param_2 = (undefined4)local_2c;
            *(undefined4 *)((int)param_2 + 4) = local_2c._4_4_;
          }
          else if (uVar3 == 0x400) {
            if (*param_2 <= _DAT_00592d98) {
              local_3c = -(double)CONCAT44(DAT_007646cc,DAT_007646c8);
            }
            else {
              local_3c = (double)CONCAT44(DAT_007646dc,DAT_007646d8);
            }
            *(undefined4 *)param_2 = (undefined4)local_3c;
            *(undefined4 *)((int)param_2 + 4) = local_3c._4_4_;
          }
        }
        else if (uVar3 == 0xc00) {
          if (*param_2 <= _DAT_00592d98) {
            local_44 = -(double)CONCAT44(DAT_007646dc,DAT_007646d8);
          }
          else {
            local_44 = (double)CONCAT44(DAT_007646dc,DAT_007646d8);
          }
          *(undefined4 *)param_2 = (undefined4)local_44;
          *(undefined4 *)((int)param_2 + 4) = local_44._4_4_;
        }
        local_8 = local_8 & 0xfffffffe;
      }
    }
    else {
      FUN__text__0057f110(4);
      local_8 = local_8 & 0xfffffffb;
    }
  }
  else {
    FUN__text__0057f110(1);
    local_8 = local_8 & 0xfffffff7;
  }
  if (((param_1 & 0x10) != 0) && ((param_3 & 0x20) != 0)) {
    FUN__text__0057f110(0x20);
    local_8 = local_8 & 0xffffffef;
  }
  return local_8 == 0;
}

