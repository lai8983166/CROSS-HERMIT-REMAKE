
float10 FUN__text__0057e260(undefined4 param_1,undefined4 param_2,undefined4 param_3,
                           undefined4 param_4,undefined4 param_5,undefined4 param_6,
                           undefined4 param_7)

{
  int iVar1;
  float10 fVar2;
  undefined1 local_60 [56];
  uint local_28;
  int local_8;
  
  iVar1 = FUN__text__0057e8c0(param_1,&param_5,param_7);
  if (iVar1 == 0) {
    local_28 = local_28 & 0xfffffffe;
    FUN__text__0057e3f0(local_60,&param_7,param_1,param_2,&param_3,&param_5);
  }
  local_8 = FUN__text__0057ed60(param_1);
  if ((DAT_00765150 == 0) && (local_8 != 0)) {
    fVar2 = (float10)__umatherr(local_8,param_2,param_3,param_4,0,0,param_5,param_6,param_7);
  }
  else {
    FID_conflict___set_errno_from_matherr(local_8);
    FUN__text__0057f0d0(param_7,0xffff);
    fVar2 = (float10)(double)CONCAT44(param_6,param_5);
  }
  return fVar2;
}

