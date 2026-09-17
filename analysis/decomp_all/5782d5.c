
undefined4 FUN__text__005782d5(void)

{
  undefined4 uVar1;
  int unaff_EBP;
  
  if (*(int *)(unaff_EBP + -0x28) == 0) {
    uVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                      (DAT_0080ab28,0x10,*(undefined4 *)(unaff_EBP + 8),
                       *(undefined4 *)(unaff_EBP + 0xc));
    *(undefined4 *)(unaff_EBP + -0x1c) = uVar1;
  }
  ExceptionList = *(void **)(unaff_EBP + -0x10);
  return *(undefined4 *)(unaff_EBP + -0x1c);
}

