
uint __thiscall FUN__text__005718c0(undefined4 param_1,int param_2)

{
  uint uVar1;
  
  if (DAT_00764370 < 2) {
    uVar1 = *(ushort *)(PTR_DAT_00764164 + param_2 * 2) & 0x80;
  }
  else {
    uVar1 = FUN__text__0057bb50(param_2,0x80,param_1);
  }
  return uVar1;
}

