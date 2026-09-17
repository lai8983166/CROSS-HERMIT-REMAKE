
void FUN__text__0057872a(void)

{
  undefined4 uVar1;
  int iVar2;
  int unaff_EBP;
  
  do {
    if ((*(int *)(unaff_EBP + -0x24) != 0) || (DAT_0080a4ec == 0)) {
      FUN__text__005787c2();
      return;
    }
    iVar2 = __callnewh(*(size_t *)(unaff_EBP + 0xc));
    if (iVar2 == 0) {
      FUN__text__005787c2();
      return;
    }
    *(undefined4 *)(unaff_EBP + -0x24) = 0;
  } while (0xffffffe0 < *(uint *)(unaff_EBP + 0xc));
  FUN__text__00577040(9);
  *(undefined4 *)(unaff_EBP + -4) = 1;
  uVar1 = FUN__text__0057ac20(*(undefined4 *)(unaff_EBP + 8),unaff_EBP + -0x38,unaff_EBP + -0x2c);
  *(undefined4 *)(unaff_EBP + -0x30) = uVar1;
  if (*(int *)(unaff_EBP + -0x30) == 0) {
    uVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                      (DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 8),
                       *(undefined4 *)(unaff_EBP + 0xc));
    *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
  }
  else {
    if (*(uint *)(unaff_EBP + 0xc) < DAT_0076415c) {
      iVar2 = FUN__text__0057b390(*(undefined4 *)(unaff_EBP + -0x38),
                                  *(undefined4 *)(unaff_EBP + -0x2c),
                                  *(undefined4 *)(unaff_EBP + -0x30),*(uint *)(unaff_EBP + 0xc) >> 4
                                 );
      if (iVar2 == 0) {
        uVar1 = FUN__text__0057ad20(*(uint *)(unaff_EBP + 0xc) >> 4);
        *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
        if (*(int *)(unaff_EBP + -0x24) != 0) {
          *(uint *)(unaff_EBP + -0x34) = (uint)**(byte **)(unaff_EBP + -0x30) << 4;
          if (*(uint *)(unaff_EBP + -0x34) < *(uint *)(unaff_EBP + 0xc)) {
            *(undefined4 *)(unaff_EBP + -0x44) = *(undefined4 *)(unaff_EBP + -0x34);
          }
          else {
            *(undefined4 *)(unaff_EBP + -0x44) = *(undefined4 *)(unaff_EBP + 0xc);
          }
          FUN__text__0056d4d0(*(undefined4 *)(unaff_EBP + -0x24),*(undefined4 *)(unaff_EBP + 8),
                              *(undefined4 *)(unaff_EBP + -0x44));
          FUN__text__0057acb0(*(undefined4 *)(unaff_EBP + -0x38),*(undefined4 *)(unaff_EBP + -0x2c),
                              *(undefined4 *)(unaff_EBP + -0x30));
        }
      }
      else {
        *(undefined4 *)(unaff_EBP + -0x24) = *(undefined4 *)(unaff_EBP + 8);
      }
    }
    if (*(int *)(unaff_EBP + -0x24) == 0) {
      uVar1 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 0xc));
      *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
      if (*(int *)(unaff_EBP + -0x24) != 0) {
        *(uint *)(unaff_EBP + -0x34) = (uint)**(byte **)(unaff_EBP + -0x30) << 4;
        if (*(uint *)(unaff_EBP + -0x34) < *(uint *)(unaff_EBP + 0xc)) {
          *(undefined4 *)(unaff_EBP + -0x48) = *(undefined4 *)(unaff_EBP + -0x34);
        }
        else {
          *(undefined4 *)(unaff_EBP + -0x48) = *(undefined4 *)(unaff_EBP + 0xc);
        }
        FUN__text__0056d4d0(*(undefined4 *)(unaff_EBP + -0x24),*(undefined4 *)(unaff_EBP + 8),
                            *(undefined4 *)(unaff_EBP + -0x48));
        FUN__text__0057acb0(*(undefined4 *)(unaff_EBP + -0x38),*(undefined4 *)(unaff_EBP + -0x2c),
                            *(undefined4 *)(unaff_EBP + -0x30));
      }
    }
  }
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  FUN__text__0057871f();
  FUN__text__0057872a();
  return;
}

