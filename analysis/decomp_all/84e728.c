
uint FUN__text1__0084e728(uint param_1)

{
  ushort uVar1;
  int iVar2;
  ushort local_6;
  
  uVar1 = (ushort)param_1;
  if (uVar1 == 0xffff) {
    return param_1;
  }
  if (DAT_008758bc == 0) {
    if ((0x40 < uVar1) && (uVar1 < 0x5b)) {
      return param_1 + 0x20;
    }
  }
  else {
    if (uVar1 < 0x100) {
      iVar2 = FUN__text1__0084e9d6(param_1,1);
      if (iVar2 == 0) {
        return param_1 & 0xffff;
      }
    }
    iVar2 = FUN__text1__0084e79d(DAT_008758bc,0x100,&param_1,1,&local_6,1,0);
    param_1 = param_1 & 0xffff;
    if (iVar2 != 0) {
      param_1 = (uint)local_6;
    }
  }
  return param_1;
}

