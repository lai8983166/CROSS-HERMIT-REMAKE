
void * FUN__text1__00849722(int param_1,int param_2)

{
  size_t _Size;
  void *_Dst;
  LPVOID pvVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  
  uVar3 = param_1 * param_2;
  uVar4 = uVar3;
  if (uVar3 < 0xffffffe1) {
    if (uVar3 == 0) {
      uVar4 = 1;
    }
    uVar4 = uVar4 + 0xf & 0xfffffff0;
  }
  do {
    if (uVar4 < 0xffffffe1) {
      if (DAT_00876b44 == 3) {
        if (uVar3 <= DAT_00876b3c) {
          _Dst = (void *)FUN__text1__0084b23f(uVar3);
          _Size = uVar3;
joined_r0x0084978b:
          if (_Dst != (void *)0x0) {
            _memset(_Dst,0,_Size);
            return _Dst;
          }
        }
      }
      else if ((DAT_00876b44 == 2) && (uVar4 <= DAT_008725cc)) {
        _Dst = (void *)FUN__text1__0084bce2(uVar4 >> 4);
        _Size = uVar4;
        goto joined_r0x0084978b;
      }
      pvVar1 = HeapAlloc(DAT_00876b40,8,uVar4);
      if (pvVar1 != (LPVOID)0x0) {
        return pvVar1;
      }
    }
    if (DAT_008757d4 == 0) {
      return (void *)0x0;
    }
    iVar2 = FUN__text1__0084920c(uVar4);
    if (iVar2 == 0) {
      return (void *)0x0;
    }
  } while( true );
}

