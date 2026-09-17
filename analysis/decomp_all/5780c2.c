
undefined4 FUN_005780c2(void)

{
  undefined4 uVar1;
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  if (*(int *)(unaff_EBP + -0x1c) == 0) {
    uVar1 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 8));
  }
  else {
    uVar1 = *(undefined4 *)(unaff_EBP + -0x1c);
  }
  *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
  return uVar1;
}

