
void FUN__text__00578513(void)

{
  undefined4 uVar1;
  int iVar2;
  int unaff_EBP;
  
  if (*(int *)(unaff_EBP + -0x28) == 0) {
    if (*(int *)(unaff_EBP + 0xc) == 0) {
      *(undefined4 *)(unaff_EBP + 0xc) = 1;
    }
    *(uint *)(unaff_EBP + 0xc) = *(int *)(unaff_EBP + 0xc) + 0xfU & 0xfffffff0;
    uVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                      (DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 8),
                       *(undefined4 *)(unaff_EBP + 0xc));
    *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
  }
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
  *(undefined4 *)(unaff_EBP + -4) = 0;
  uVar1 = FUN__text__00578c00(*(undefined4 *)(unaff_EBP + 8));
  *(undefined4 *)(unaff_EBP + -0x28) = uVar1;
  if (*(int *)(unaff_EBP + -0x28) != 0) {
    if (*(uint *)(unaff_EBP + 0xc) <= DAT_0080ab4c) {
      iVar2 = FUN__text__00579ae0(*(undefined4 *)(unaff_EBP + -0x28),*(undefined4 *)(unaff_EBP + 8),
                                  *(undefined4 *)(unaff_EBP + 0xc));
      if (iVar2 == 0) {
        uVar1 = FUN__text__005792a0(*(undefined4 *)(unaff_EBP + 0xc));
        *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
        if (*(int *)(unaff_EBP + -0x24) != 0) {
          *(int *)(unaff_EBP + -0x20) = *(int *)(*(int *)(unaff_EBP + 8) + -4) + -1;
          if (*(uint *)(unaff_EBP + -0x20) < *(uint *)(unaff_EBP + 0xc)) {
            *(undefined4 *)(unaff_EBP + -0x3c) = *(undefined4 *)(unaff_EBP + -0x20);
          }
          else {
            *(undefined4 *)(unaff_EBP + -0x3c) = *(undefined4 *)(unaff_EBP + 0xc);
          }
          FUN__text__0056d4d0(*(undefined4 *)(unaff_EBP + -0x24),*(undefined4 *)(unaff_EBP + 8),
                              *(undefined4 *)(unaff_EBP + -0x3c));
          uVar1 = FUN__text__00578c00(*(undefined4 *)(unaff_EBP + 8));
          *(undefined4 *)(unaff_EBP + -0x28) = uVar1;
          FUN__text__00578cc0(*(undefined4 *)(unaff_EBP + -0x28),*(undefined4 *)(unaff_EBP + 8));
        }
      }
      else {
        *(undefined4 *)(unaff_EBP + -0x24) = *(undefined4 *)(unaff_EBP + 8);
      }
    }
    if (*(int *)(unaff_EBP + -0x24) == 0) {
      if (*(int *)(unaff_EBP + 0xc) == 0) {
        *(undefined4 *)(unaff_EBP + 0xc) = 1;
      }
      *(uint *)(unaff_EBP + 0xc) = *(int *)(unaff_EBP + 0xc) + 0xfU & 0xfffffff0;
      uVar1 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 0xc));
      *(undefined4 *)(unaff_EBP + -0x24) = uVar1;
      if (*(int *)(unaff_EBP + -0x24) != 0) {
        *(int *)(unaff_EBP + -0x20) = *(int *)(*(int *)(unaff_EBP + 8) + -4) + -1;
        if (*(uint *)(unaff_EBP + -0x20) < *(uint *)(unaff_EBP + 0xc)) {
          *(undefined4 *)(unaff_EBP + -0x40) = *(undefined4 *)(unaff_EBP + -0x20);
        }
        else {
          *(undefined4 *)(unaff_EBP + -0x40) = *(undefined4 *)(unaff_EBP + 0xc);
        }
        FUN__text__0056d4d0(*(undefined4 *)(unaff_EBP + -0x24),*(undefined4 *)(unaff_EBP + 8),
                            *(undefined4 *)(unaff_EBP + -0x40));
        FUN__text__00578cc0(*(undefined4 *)(unaff_EBP + -0x28),*(undefined4 *)(unaff_EBP + 8));
      }
    }
  }
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  FUN__text__00578508();
  FUN__text__00578513();
  return;
}

