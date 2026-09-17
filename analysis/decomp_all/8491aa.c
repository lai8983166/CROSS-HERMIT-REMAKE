
undefined4 FUN__text1__008491aa(undefined1 *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  undefined1 *local_24;
  int local_20;
  undefined1 *local_1c;
  undefined4 local_18;
  
  local_1c = param_1;
  local_24 = param_1;
  local_18 = 0x42;
  local_20 = 0x7fffffff;
  uVar1 = FUN__text1__00849a03(&local_24,param_2,&stack0x0000000c);
  local_20 = local_20 + -1;
  if (local_20 < 0) {
    FUN__text1__008498ee(0,&local_24);
  }
  else {
    *local_24 = 0;
  }
  return uVar1;
}

