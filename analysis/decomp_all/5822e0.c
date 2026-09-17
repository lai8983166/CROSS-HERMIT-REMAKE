
bool FUN__text__005822e0(undefined4 param_1)

{
  int iVar1;
  int iVar2;
  size_t sVar3;
  uint uVar4;
  bool bVar5;
  undefined1 local_7c [120];
  
  iVar1 = FUN__text__00582c40(param_1);
  iVar2 = (*DAT_0080a688)(iVar1,(-(uint)(DAT_0080a66c != 0) & 0xfffff005) + 0x1002,local_7c,0x78);
  if (iVar2 == 0) {
    DAT_0080a680 = 0;
    bVar5 = true;
  }
  else {
    iVar2 = FUN__text__0058af40(DAT_0080a67c,local_7c);
    if (iVar2 == 0) {
      iVar2 = (*DAT_0080a688)(iVar1,(-(uint)(DAT_0080a674 != 0) & 0xfffff002) + 0x1001,local_7c,0x78
                             );
      if (iVar2 == 0) {
        DAT_0080a680 = 0;
        return true;
      }
      iVar2 = FUN__text__0058af40(DAT_0080a678,local_7c);
      if (iVar2 == 0) {
        DAT_0080a680 = DAT_0080a680 | 0x304;
        DAT_0080a668 = iVar1;
        DAT_0080a684 = iVar1;
      }
      else if ((DAT_0080a680 & 2) == 0) {
        if ((DAT_0080a670 == 0) ||
           (iVar2 = FUN__text__0058b010(DAT_0080a678,local_7c,DAT_0080a670), iVar2 != 0)) {
          if (((DAT_0080a680 & 1) == 0) && (iVar2 = FUN__text__00582980(iVar1), iVar2 != 0)) {
            DAT_0080a680 = DAT_0080a680 | 1;
            DAT_0080a684 = iVar1;
          }
        }
        else {
          DAT_0080a680 = DAT_0080a680 | 2;
          DAT_0080a684 = iVar1;
          sVar3 = _strlen(DAT_0080a678);
          if (sVar3 == DAT_0080a670) {
            DAT_0080a668 = iVar1;
          }
        }
      }
    }
    if ((DAT_0080a680 & 0x300) != 0x300) {
      iVar2 = (*DAT_0080a688)(iVar1,(-(uint)(DAT_0080a674 != 0) & 0xfffff002) + 0x1001,local_7c,0x78
                             );
      if (iVar2 == 0) {
        DAT_0080a680 = 0;
        return true;
      }
      iVar2 = FUN__text__0058af40(DAT_0080a678,local_7c);
      if (iVar2 == 0) {
        uVar4 = DAT_0080a680 | 0x200;
        if (DAT_0080a674 == 0) {
          DAT_0080a680 = uVar4;
          if ((DAT_0080a670 == 0) || (sVar3 = _strlen(DAT_0080a678), sVar3 != DAT_0080a670)) {
            DAT_0080a680 = DAT_0080a680 | 0x100;
            if (DAT_0080a668 == 0) {
              DAT_0080a668 = iVar1;
            }
          }
          else {
            iVar2 = FUN__text__005829d0(iVar1,1);
            if ((iVar2 != 0) && (DAT_0080a680 = DAT_0080a680 | 0x100, DAT_0080a668 == 0)) {
              DAT_0080a668 = iVar1;
            }
          }
        }
        else {
          DAT_0080a680 = DAT_0080a680 | 0x300;
          if (DAT_0080a668 == 0) {
            DAT_0080a668 = iVar1;
          }
        }
      }
      else if ((((DAT_0080a674 == 0) && (DAT_0080a670 != 0)) &&
               (iVar2 = FUN__text__0058b010(DAT_0080a678,local_7c,DAT_0080a670), iVar2 == 0)) &&
              ((iVar2 = FUN__text__005829d0(iVar1,0), iVar2 != 0 &&
               (DAT_0080a680 = DAT_0080a680 | 0x100, DAT_0080a668 == 0)))) {
        DAT_0080a668 = iVar1;
      }
    }
    bVar5 = (DAT_0080a680 & 4) == 0;
  }
  return bVar5;
}

