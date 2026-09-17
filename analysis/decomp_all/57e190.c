
float10 FUN__text__0057e190(undefined4 param_1,undefined4 param_2,undefined4 param_3,
                           undefined4 param_4)

{
  undefined4 *puVar1;
  float10 fVar2;
  
  if (DAT_00765150 == 0) {
    fVar2 = (float10)__umatherr(1,param_1,param_2,param_3,0,0,param_2,param_3,param_4);
  }
  else {
    puVar1 = (undefined4 *)FUN__text__00576d20();
    *puVar1 = 0x21;
    FUN__text__0057f0d0(param_4,0xffff);
    fVar2 = (float10)(double)CONCAT44(param_3,param_2);
  }
  return fVar2;
}

