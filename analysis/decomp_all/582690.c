
bool FUN__text__00582690(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  bool bVar3;
  undefined1 local_7c [120];
  
  uVar1 = FUN__text__00582c40(param_1);
  iVar2 = (*DAT_0080a688)(uVar1,(-(uint)(DAT_0080a674 != 0) & 0xfffff002) + 0x1001,local_7c,0x78);
  if (iVar2 == 0) {
    DAT_0080a680 = 0;
    bVar3 = true;
  }
  else {
    iVar2 = FUN__text__0058af40(DAT_0080a678,local_7c);
    if (iVar2 == 0) {
      if ((DAT_0080a674 != 0) || (iVar2 = FUN__text__005829d0(uVar1,1), iVar2 != 0)) {
        DAT_0080a680 = DAT_0080a680 | 4;
        DAT_0080a668 = uVar1;
        DAT_0080a684 = uVar1;
      }
    }
    else if ((((DAT_0080a674 == 0) && (DAT_0080a670 != 0)) &&
             (iVar2 = FUN__text__0058b010(DAT_0080a678,local_7c,DAT_0080a670), iVar2 == 0)) &&
            (iVar2 = FUN__text__005829d0(uVar1,0), iVar2 != 0)) {
      DAT_0080a680 = DAT_0080a680 | 4;
      DAT_0080a668 = uVar1;
      DAT_0080a684 = uVar1;
    }
    bVar3 = (DAT_0080a680 & 4) == 0;
  }
  return bVar3;
}

