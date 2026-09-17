
byte * __fastcall FUN__text__0057cc70(undefined4 param_1)

{
  byte *pbVar1;
  int iVar2;
  byte *pbVar3;
  
  if (DAT_0080bb80 == 0) {
    FUN__text__0057c3f0(param_1);
  }
  pbVar3 = DAT_0080bb74;
  pbVar1 = DAT_0080bb74;
  if (*DAT_0080bb74 == 0x22) {
    while ((pbVar1 = pbVar3 + 1, *pbVar1 != 0x22 && (*pbVar1 != 0))) {
      iVar2 = FUN__text__00588190(*pbVar1);
      pbVar3 = pbVar1;
      if (iVar2 != 0) {
        pbVar3 = pbVar1 + 1;
      }
    }
    if (*pbVar1 == 0x22) {
      pbVar1 = pbVar3 + 2;
    }
  }
  else {
    for (; 0x20 < *pbVar1; pbVar1 = pbVar1 + 1) {
    }
  }
  for (; (*pbVar1 != 0 && (*pbVar1 < 0x21)); pbVar1 = pbVar1 + 1) {
  }
  return pbVar1;
}

