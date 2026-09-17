
int FUN__text1__0084d517(int param_1)

{
  int iVar1;
  
  if (param_1 == 0) {
    iVar1 = flsall(0);
    return iVar1;
  }
  iVar1 = FUN__text1__0084d552(param_1);
  if (iVar1 != 0) {
    return -1;
  }
  if ((*(byte *)(param_1 + 0xd) & 0x40) != 0) {
    iVar1 = FUN__text1__0084daa2(*(undefined4 *)(param_1 + 0x10));
    return -(uint)(iVar1 != 0);
  }
  return 0;
}

