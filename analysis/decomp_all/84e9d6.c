
uint FUN__text1__0084e9d6(ushort param_1,ushort param_2)

{
  int iVar1;
  uint local_8;
  
  if (param_1 == 0xffff) {
    return 0;
  }
  if (param_1 < 0x100) {
    local_8 = (uint)*(ushort *)(PTR_DAT_00870264 + (uint)param_1 * 2);
  }
  else {
    iVar1 = FUN__text1__0084ea28(1,&param_1,1,&local_8,0,0);
    if (iVar1 == 0) {
      return 0;
    }
  }
  return local_8 & 0xffff & (uint)param_2;
}

