
void FUN_005780e1(void)

{
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  if (*(int *)(unaff_EBP + 8) == 0) {
    *(undefined4 *)(unaff_EBP + 8) = 1;
  }
  *(uint *)(unaff_EBP + 8) = *(int *)(unaff_EBP + 8) + 0xfU & 0xfffffff0;
  (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 8));
  *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
  return;
}

