
int FUN__text1__0084e52c(ushort *param_1,ushort *param_2)

{
  ushort uVar1;
  ushort uVar2;
  
  if (DAT_008758bc == 0) {
    do {
      uVar1 = *param_1;
      if ((uVar1 < 0x5b) && (0x40 < uVar1)) {
        uVar1 = uVar1 + 0x20;
      }
      uVar2 = *param_2;
      if ((uVar2 < 0x5b) && (0x40 < uVar2)) {
        uVar2 = uVar2 + 0x20;
      }
      param_1 = param_1 + 1;
      param_2 = param_2 + 1;
    } while ((uVar1 != 0) && (uVar1 == uVar2));
  }
  else {
    do {
      uVar1 = *param_1;
      param_1 = param_1 + 1;
      uVar1 = FUN__text1__0084e728(uVar1);
      uVar2 = *param_2;
      param_2 = param_2 + 1;
      uVar2 = FUN__text1__0084e728(uVar2);
      if (uVar1 == 0) break;
    } while (uVar1 == uVar2);
  }
  return (uint)uVar1 - (uint)uVar2;
}

