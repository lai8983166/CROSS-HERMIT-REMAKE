
byte * __thiscall FUN__text__0058e7e0(undefined4 param_1,byte *param_2,uint param_3)

{
  ushort uVar1;
  byte *pbVar2;
  uint uVar3;
  
  if (DAT_0080a91c == 0) {
    param_2 = (byte *)_strchr((char *)param_2,param_3);
  }
  else {
    FUN__text__00577040(0x19,param_1);
    while( true ) {
      uVar1 = (ushort)*param_2;
      uVar3 = (uint)uVar1;
      if (uVar1 == 0) break;
      if (((&DAT_0080aa21)[uVar1] & 4) == 0) {
        pbVar2 = param_2;
        if (param_3 == uVar1) break;
      }
      else {
        pbVar2 = param_2 + 1;
        if (*pbVar2 == 0) {
          FUN__text__005770e0(0x19);
          return (byte *)0x0;
        }
        if (param_3 == CONCAT11(*param_2,*pbVar2)) {
          FUN__text__005770e0(0x19);
          return param_2;
        }
      }
      param_2 = pbVar2;
      param_2 = param_2 + 1;
    }
    FUN__text__005770e0(0x19);
    if (param_3 != (uVar3 & 0xffff)) {
      param_2 = (byte *)0x0;
    }
  }
  return param_2;
}

