
bool FUN__text__00582800(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  bool bVar3;
  undefined1 local_7c [120];
  
  uVar1 = FUN__text__00582c40(param_1);
  iVar2 = (*DAT_0080a688)(uVar1,(-(uint)(DAT_0080a66c != 0) & 0xfffff005) + 0x1002,local_7c,0x78);
  if (iVar2 == 0) {
    DAT_0080a680 = 0;
    bVar3 = true;
  }
  else {
    iVar2 = FUN__text__0058af40(DAT_0080a67c,local_7c);
    if (iVar2 == 0) {
      iVar2 = FUN__text__00582980(uVar1);
      if (iVar2 != 0) {
        DAT_0080a680 = DAT_0080a680 | 4;
        DAT_0080a668 = uVar1;
        DAT_0080a684 = uVar1;
      }
    }
    bVar3 = (DAT_0080a680 & 4) == 0;
  }
  return bVar3;
}

