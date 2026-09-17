
int FUN__text__00577570(int param_1)

{
  int iVar1;
  
  iVar1 = FUN__text__005775c0(param_1);
  if (iVar1 == 0) {
    if ((*(uint *)(param_1 + 0xc) & 0x4000) == 0) {
      iVar1 = 0;
    }
    else {
      iVar1 = FUN__text__005866e0(*(undefined4 *)(param_1 + 0x10));
      iVar1 = -(uint)(iVar1 != 0);
    }
  }
  else {
    iVar1 = -1;
  }
  return iVar1;
}

