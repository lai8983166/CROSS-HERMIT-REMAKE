
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__005721a0(int param_1,uint param_2,int param_3,uint param_4)

{
  double dVar1;
  undefined4 unaff_EBP;
  float10 fVar2;
  int local_20;
  double local_1c;
  int local_14;
  undefined4 local_10;
  int local_c;
  undefined4 uStack_8;
  undefined2 uStack_4;
  undefined2 uStack_2;
  
  uStack_4 = (undefined2)unaff_EBP;
  uStack_2 = (undefined2)((uint)unaff_EBP >> 0x10);
  local_10 = FUN__text__0057f0d0();
  if (((param_2._2_2_ & 0x7ff0) == 0x7ff0) || ((param_4._2_2_ & 0x7ff0) == 0x7ff0)) {
    if ((((param_2._2_2_ & 0x7ff8) == 0x7ff0) && (((param_2 & 0x7ffff) != 0 || (param_1 != 0)))) ||
       (((param_4._2_2_ & 0x7ff8) == 0x7ff0 && (((param_4 & 0x7ffff) != 0 || (param_3 != 0)))))) {
      fVar2 = (float10)FUN__text__0057e320(8,0x26,param_1,param_2,param_3,param_4,
                                           (double)CONCAT26(param_2._2_2_,
                                                            CONCAT24((undefined2)param_2,param_1)) +
                                           (double)CONCAT26(param_4._2_2_,
                                                            CONCAT24((undefined2)param_4,param_3)),
                                           local_10);
      return fVar2;
    }
    if (((param_2._2_2_ & 0x7ff8) == 0x7ff8) || ((param_4._2_2_ & 0x7ff8) == 0x7ff8)) {
      fVar2 = (float10)FUN__text__0057e1f0(0x26,param_1,param_2,param_3,param_4,local_10);
      return fVar2;
    }
  }
  if ((double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)) ==
      (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1))) {
    FUN__text__0057f0d0();
    fVar2 = (float10)(double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1));
  }
  else {
    if ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) == _DAT_00592d98) {
      local_c = 1;
      if ((double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)) <=
          (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1))) {
        uStack_8._0_2_ = 0;
        uStack_8._2_2_ = 0x8000;
      }
      else {
        uStack_8._0_2_ = 0;
        uStack_8._2_2_ = 0;
      }
    }
    if (((_DAT_00592d98 < (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1))) &&
        ((double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)) <
         (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)))) ||
       (((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) < _DAT_00592d98 &&
        ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) <
         (double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)))))) {
      local_c = param_1 + -1;
      uStack_8 = param_2;
      if (param_1 == 0) {
        uStack_8 = param_2 - 1;
      }
    }
    else if ((((_DAT_00592d98 <
                (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1))) &&
              ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) <
               (double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)))) ||
             ((uStack_8 = CONCAT22(uStack_8._2_2_,(undefined2)uStack_8),
              (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) < _DAT_00592d98
              && (uStack_8 = CONCAT22(uStack_8._2_2_,(undefined2)uStack_8),
                 (double)CONCAT26(param_4._2_2_,CONCAT24((undefined2)param_4,param_3)) <
                 (double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)))))) &&
            (local_c = param_1 + 1, uStack_8 = param_2, local_c == 0)) {
      uStack_8 = param_2 + 1;
    }
    if (((uStack_8 & 0x7ff00000) == 0) && (((uStack_8 & 0xfffff) != 0 || (local_c != 0)))) {
      fVar2 = (float10)FUN__text__0057ef50(local_c,uStack_8,&local_14);
      local_1c = (double)fVar2;
      fVar2 = (float10)FUN__text__0057ede0(local_1c,local_14 + 0x600);
      dVar1 = (double)fVar2;
      local_c = SUB84(dVar1,0);
      uStack_8._0_2_ = (undefined2)((ulonglong)dVar1 >> 0x20);
      uStack_8._2_2_ = (undefined2)((ulonglong)dVar1 >> 0x30);
      fVar2 = (float10)FUN__text__0057e320(0x12,0x26,param_1,param_2,param_3,param_4,dVar1,local_10)
      ;
    }
    else if (((uStack_8 == 0x7ff00000) && (local_c == 0)) ||
            ((uStack_8 == 0xfff00000 && (local_c == 0)))) {
      fVar2 = (float10)FUN__text__0057ef50(local_c,uStack_8,&local_20);
      fVar2 = (float10)FUN__text__0057ede0((double)fVar2,local_20 + -0x600);
      dVar1 = (double)fVar2;
      local_c = SUB84(dVar1,0);
      uStack_8._0_2_ = (undefined2)((ulonglong)dVar1 >> 0x20);
      uStack_8._2_2_ = (undefined2)((ulonglong)dVar1 >> 0x30);
      fVar2 = (float10)FUN__text__0057e320(0x11,0x26,param_1,param_2,param_3,param_4,dVar1,local_10)
      ;
    }
    else {
      FUN__text__0057f0d0();
      fVar2 = (float10)(double)CONCAT26(uStack_8._2_2_,CONCAT24((undefined2)uStack_8,local_c));
    }
  }
  return fVar2;
}

