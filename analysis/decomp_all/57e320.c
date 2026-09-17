
float10 FUN__text__0057e320(undefined4 param_1,undefined4 param_2,undefined4 param_3,
                           undefined4 param_4,undefined4 param_5,undefined4 param_6,
                           undefined4 param_7,undefined4 param_8,undefined4 param_9)

{
  int iVar1;
  float10 fVar2;
  undefined1 local_60 [40];
  undefined4 local_38;
  undefined4 local_34;
  uint local_28;
  int local_8;
  
  iVar1 = FUN__text__0057e8c0(param_1,&param_7,param_9);
  if (iVar1 == 0) {
    local_28 = local_28 & 0xffffffe1 | 3;
    local_38 = param_5;
    local_34 = param_6;
    FUN__text__0057e3f0(local_60,&param_9,param_1,param_2,&param_3,&param_7);
  }
  local_8 = FUN__text__0057ed60(param_1);
  if ((DAT_00765150 == 0) && (local_8 != 0)) {
    fVar2 = (float10)__umatherr(local_8,param_2,param_3,param_4,param_5,param_6,param_7,param_8,
                                param_9);
  }
  else {
    FID_conflict___set_errno_from_matherr(local_8);
    FUN__text__0057f0d0(param_9,0xffff);
    fVar2 = (float10)(double)CONCAT44(param_8,param_7);
  }
  return fVar2;
}

