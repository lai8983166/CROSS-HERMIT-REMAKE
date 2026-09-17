
void FUN_00578866(void)

{
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  if (*(int *)(unaff_EBP + -0x1c) == 0) {
    (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,*(undefined4 *)(unaff_EBP + 8));
  }
  *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
  return;
}

