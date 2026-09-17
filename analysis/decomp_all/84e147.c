
void * __thiscall FUN__text1__0084e147(undefined4 param_1,LPVOID param_2,uint param_3)

{
  void *pvVar1;
  int iVar2;
  int iVar3;
  LPVOID pvVar4;
  uint uVar5;
  byte *pbVar6;
  uint uVar7;
  undefined4 local_8;
  
  local_8 = param_1;
  if (param_2 == (LPVOID)0x0) {
    pvVar1 = _malloc(param_3);
  }
  else {
    if (param_3 == 0) {
      FUN__text1__008497d3(param_2);
    }
    else {
      uVar7 = param_3;
      if (DAT_00876b44 == 3) {
        do {
          if (uVar7 < 0xffffffe1) {
            iVar2 = FUN__text1__0084aeeb(param_2);
            if (iVar2 == 0) {
LAB__text1__0084e23e:
              if (uVar7 == 0) {
                uVar7 = 1;
              }
              uVar7 = uVar7 + 0xf & 0xfffffff0;
              pvVar4 = HeapReAlloc(DAT_00876b40,0,param_2,uVar7);
            }
            else {
              if (DAT_00876b3c < uVar7) {
LAB__text1__0084e1f7:
                if (uVar7 == 0) {
                  uVar7 = 1;
                }
                uVar7 = uVar7 + 0xf & 0xfffffff0;
                pvVar4 = HeapAlloc(DAT_00876b40,0,uVar7);
                if (pvVar4 != (LPVOID)0x0) {
                  uVar5 = *(int *)((int)param_2 + -4) - 1;
                  if (uVar7 <= uVar5) {
                    uVar5 = uVar7;
                  }
                  FUN__text1__00848490(pvVar4,param_2,uVar5);
                  FUN__text1__0084af16(iVar2,param_2);
                }
              }
              else {
                iVar3 = FUN__text1__0084b6f4(iVar2,param_2,uVar7);
                pvVar4 = param_2;
                if (iVar3 == 0) {
                  pvVar4 = (LPVOID)FUN__text1__0084b23f(uVar7);
                  if (pvVar4 == (LPVOID)0x0) goto LAB__text1__0084e1f7;
                  uVar5 = *(int *)((int)param_2 + -4) - 1;
                  if (uVar7 <= uVar5) {
                    uVar5 = uVar7;
                  }
                  FUN__text1__00848490(pvVar4,param_2,uVar5);
                  iVar2 = FUN__text1__0084aeeb(param_2);
                  FUN__text1__0084af16(iVar2,param_2);
                }
                if (pvVar4 == (LPVOID)0x0) goto LAB__text1__0084e1f7;
              }
              if (iVar2 == 0) goto LAB__text1__0084e23e;
            }
            if (pvVar4 != (LPVOID)0x0) {
              return pvVar4;
            }
          }
          if (DAT_008757d4 == 0) {
            return (void *)0x0;
          }
          iVar2 = FUN__text1__0084920c(uVar7);
        } while (iVar2 != 0);
      }
      else if (DAT_00876b44 == 2) {
        if (param_3 < 0xffffffe1) {
          if (param_3 == 0) {
            uVar7 = 0x10;
          }
          else {
            uVar7 = param_3 + 0xf & 0xfffffff0;
          }
        }
        do {
          if (uVar7 < 0xffffffe1) {
            pbVar6 = (byte *)FUN__text1__0084bc46(param_2,&local_8,&param_3);
            if (pbVar6 == (byte *)0x0) {
              pvVar4 = HeapReAlloc(DAT_00876b40,0,param_2,uVar7);
            }
            else {
              if (uVar7 < DAT_008725cc) {
                iVar2 = FUN__text1__0084c00e(local_8,param_3,pbVar6,uVar7 >> 4);
                pvVar4 = param_2;
                if (iVar2 == 0) {
                  pvVar4 = (LPVOID)FUN__text1__0084bce2(uVar7 >> 4);
                  if (pvVar4 == (LPVOID)0x0) goto LAB__text1__0084e32c;
                  uVar5 = (uint)*pbVar6 << 4;
                  if (uVar7 <= (uint)*pbVar6 << 4) {
                    uVar5 = uVar7;
                  }
                  FUN__text1__00848490(pvVar4,param_2,uVar5);
                  FUN__text1__0084bc9d(local_8,param_3,pbVar6);
                }
                if (pvVar4 != (LPVOID)0x0) {
                  return pvVar4;
                }
              }
LAB__text1__0084e32c:
              pvVar4 = HeapAlloc(DAT_00876b40,0,uVar7);
              if (pvVar4 == (LPVOID)0x0) goto LAB__text1__0084e384;
              uVar5 = (uint)*pbVar6 << 4;
              if (uVar7 <= (uint)*pbVar6 << 4) {
                uVar5 = uVar7;
              }
              FUN__text1__00848490(pvVar4,param_2,uVar5);
              FUN__text1__0084bc9d(local_8,param_3,pbVar6);
            }
            if (pvVar4 != (LPVOID)0x0) {
              return pvVar4;
            }
          }
LAB__text1__0084e384:
          if (DAT_008757d4 == 0) {
            return (void *)0x0;
          }
          iVar2 = FUN__text1__0084920c(uVar7);
        } while (iVar2 != 0);
      }
      else {
        do {
          if (uVar7 < 0xffffffe1) {
            if (uVar7 == 0) {
              uVar7 = 1;
            }
            uVar7 = uVar7 + 0xf & 0xfffffff0;
            pvVar4 = HeapReAlloc(DAT_00876b40,0,param_2,uVar7);
            if (pvVar4 != (LPVOID)0x0) {
              return pvVar4;
            }
          }
          if (DAT_008757d4 == 0) {
            return (void *)0x0;
          }
          iVar2 = FUN__text1__0084920c(uVar7);
        } while (iVar2 != 0);
      }
    }
    pvVar1 = (void *)0x0;
  }
  return pvVar1;
}

