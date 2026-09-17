
void FUN__text1__0084987a(uint param_1)

{
  int iVar1;
  uint dwBytes;
  
  if (DAT_00876b44 == 3) {
    if ((param_1 <= DAT_00876b3c) && (iVar1 = FUN__text1__0084b23f(param_1), iVar1 != 0)) {
      return;
    }
  }
  else if (DAT_00876b44 == 2) {
    if (param_1 == 0) {
      dwBytes = 0x10;
    }
    else {
      dwBytes = param_1 + 0xf & 0xfffffff0;
    }
    if ((dwBytes <= DAT_008725cc) && (iVar1 = FUN__text1__0084bce2(dwBytes >> 4), iVar1 != 0)) {
      return;
    }
    goto LAB__text1__008498dd;
  }
  if (param_1 == 0) {
    param_1 = 1;
  }
  dwBytes = param_1 + 0xf & 0xfffffff0;
LAB__text1__008498dd:
  HeapAlloc(DAT_00876b40,0,dwBytes);
  return;
}

