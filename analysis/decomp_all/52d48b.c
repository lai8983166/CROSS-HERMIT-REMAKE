
undefined4 FUN__text__0052d48b(short *param_1,uint param_2)

{
  undefined4 uVar1;
  
  if (((param_2 < 0xe) || (*param_1 != 0x4d42)) || (param_2 < *(uint *)(param_1 + 1))) {
    uVar1 = 0x80004005;
  }
  else {
    uVar1 = FUN__text__0052b1fa(param_1 + 7,param_2 - 0xe);
  }
  return uVar1;
}

