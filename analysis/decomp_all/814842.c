
uint FUN__text1__00814842(uint param_1,byte param_2,byte param_3)

{
  uint uVar1;
  uint uVar2;
  
  uVar1 = (1 << (param_2 & 0x1f)) - 1;
  uVar2 = uVar1 << (param_3 & 0x1f);
  return param_1 & ~(uVar1 | uVar2) |
         (param_1 & uVar1) << (param_3 & 0x1f) | (param_1 & uVar2) >> (param_3 & 0x1f);
}

