
undefined4 FUN__text__005781dc(void)

{
  undefined4 uVar1;
  int unaff_EBP;
  
  if (*(int *)(unaff_EBP + -0x20) == 0) {
    if (*(int *)(unaff_EBP + 0xc) == 0) {
      *(undefined4 *)(unaff_EBP + 0xc) = 1;
    }
    *(uint *)(unaff_EBP + 0xc) = *(int *)(unaff_EBP + 0xc) + 0xfU & 0xfffffff0;
    uVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                      (DAT_0080ab28,0x10,*(undefined4 *)(unaff_EBP + 8),
                       *(undefined4 *)(unaff_EBP + 0xc));
    *(undefined4 *)(unaff_EBP + -0x1c) = uVar1;
  }
  ExceptionList = *(void **)(unaff_EBP + -0x10);
  return *(undefined4 *)(unaff_EBP + -0x1c);
}

