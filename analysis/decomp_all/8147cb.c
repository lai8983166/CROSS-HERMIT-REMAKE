
uint FUN__text1__008147cb(uint param_1,int param_2,byte param_3,int param_4)

{
  uint uVar1;
  uint uVar2;
  
  if (param_4 < 0) {
    param_4 = param_4 + param_2;
  }
  uVar2 = (1 << ((byte)param_2 & 0x1f)) - 1;
  uVar1 = param_1 >> (param_3 & 0x1f) & uVar2;
  return param_1 & ~(uVar2 << (param_3 & 0x1f)) |
         ((uVar1 >> ((byte)param_4 & 0x1f) | uVar1 << ((byte)param_2 - (byte)param_4 & 0x1f)) &
         uVar2) << (param_3 & 0x1f);
}

