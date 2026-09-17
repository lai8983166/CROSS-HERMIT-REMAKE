
float10 FUN__text__0057e1f0(undefined4 param_1,undefined4 param_2,undefined4 param_3,
                           undefined4 param_4,undefined4 param_5,undefined4 param_6)

{
  double dVar1;
  undefined4 *puVar2;
  float10 fVar3;
  
  dVar1 = (double)CONCAT44(param_3,param_2) + (double)CONCAT44(param_5,param_4);
  if (DAT_00765150 == 0) {
    fVar3 = (float10)__umatherr(1,param_1,param_2,param_3,param_4,param_5,dVar1,param_6);
  }
  else {
    puVar2 = (undefined4 *)FUN__text__00576d20();
    *puVar2 = 0x21;
    FUN__text__0057f0d0(param_6,0xffff);
    fVar3 = (float10)dVar1;
  }
  return fVar3;
}

