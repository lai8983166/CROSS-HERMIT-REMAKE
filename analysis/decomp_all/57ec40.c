
/* Library Function - Single Match
    __umatherr
   
   Library: Visual Studio */

float10 __umatherr(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                  undefined4 param_5,undefined4 param_6,undefined4 param_7,undefined4 param_8,
                  undefined4 param_9)

{
  double dVar1;
  int iVar2;
  _exception local_24;
  
  local_24.name = (char *)__get_fname(param_2);
  if (local_24.name == (char *)0x0) {
    FUN__text__0057f0d0(param_9,0xffff);
    FID_conflict___set_errno_from_matherr(param_1);
    dVar1 = (double)CONCAT44(param_8,param_7);
  }
  else {
    local_24.type = param_1;
    local_24.arg1._0_4_ = param_3;
    local_24.arg1._4_4_ = param_4;
    local_24.arg2._0_4_ = param_5;
    local_24.arg2._4_4_ = param_6;
    local_24.retval._0_4_ = param_7;
    local_24.retval._4_4_ = param_8;
    FUN__text__0057f0d0(param_9,0xffff);
    iVar2 = __matherr(&local_24);
    if (iVar2 == 0) {
      FID_conflict___set_errno_from_matherr(param_1);
    }
    dVar1 = (double)CONCAT44(local_24.retval._4_4_,local_24.retval._0_4_);
  }
  return (float10)dVar1;
}

