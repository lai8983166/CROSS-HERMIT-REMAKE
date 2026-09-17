
uint FUN__text__005711ed(uint param_1,uint param_2)

{
  uint uVar1;
  bool in_ZF;
  short in_FPUControlWord;
  
  if (in_ZF) {
    if (((param_2 & 0xfffff) != 0) || (param_1 != 0)) {
      uVar1 = FUN__text__005769dc();
      goto LAB__text__0057126b;
    }
    param_1 = param_2 & 0x80000000;
    param_2 = 0;
joined_r0x0057125c:
    if (param_1 == 0) {
LAB__text__0057120e:
      if (DAT_0080a3e0 != 0) {
        return param_2;
      }
      uVar1 = __math_exit();
      return uVar1;
    }
  }
  else {
    if (in_FPUControlWord != 0x27f) {
      param_2 = FUN__text__005769c5();
    }
    if ((param_2 & 0x80000000) == 0) goto LAB__text__0057120e;
    if (((param_2 & 0x7ff00000) == 0) && ((param_2 & 0xfffff) == 0)) goto joined_r0x0057125c;
  }
  uVar1 = 1;
LAB__text__0057126b:
  if (DAT_0080a3e0 != 0) {
    return uVar1;
  }
  uVar1 = __startOneArgErrorHandling();
  return uVar1;
}

