
undefined4 FUN__text__005775c0(int *param_1)

{
  int iVar1;
  int iVar2;
  undefined4 local_8;
  
  local_8 = 0;
  if ((((param_1[3] & 3U) == 2) && ((param_1[3] & 0x108U) != 0)) &&
     (iVar2 = *param_1 - param_1[2], 0 < iVar2)) {
    iVar1 = FUN__text__0057c550(param_1[4],param_1[2],iVar2);
    if (iVar1 == iVar2) {
      if ((param_1[3] & 0x80U) != 0) {
        param_1[3] = param_1[3] & 0xfffffffd;
      }
    }
    else {
      param_1[3] = param_1[3] | 0x20;
      local_8 = 0xffffffff;
    }
  }
  *param_1 = param_1[2];
  param_1[1] = 0;
  return local_8;
}

