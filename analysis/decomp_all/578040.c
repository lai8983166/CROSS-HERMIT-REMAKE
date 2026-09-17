
undefined4 FUN_00578040(void)

{
  undefined4 uVar1;
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  if (*(int *)(unaff_EBP + -0x1c) != 0) {
    uVar1 = *(undefined4 *)(unaff_EBP + -0x1c);
    *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
    return uVar1;
  }
  uVar1 = FUN_005780e1();
  return uVar1;
}

