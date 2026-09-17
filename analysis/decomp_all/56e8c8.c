
undefined4 FUN_0056e8c8(void)

{
  int iVar1;
  undefined4 uVar2;
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  if ((*(int *)(unaff_EBP + -0x1c) == 0) && (*(int *)(unaff_EBP + 0xc) != 0)) {
    iVar1 = __callnewh(*(size_t *)(unaff_EBP + 8));
    if (iVar1 != 0) {
      FUN_00577040(9);
      *(undefined4 *)(unaff_EBP + -4) = 0;
      uVar2 = FUN_0056e920(*(undefined4 *)(unaff_EBP + 8),*(undefined4 *)(unaff_EBP + 0x10),
                           *(undefined4 *)(unaff_EBP + 0x14),*(undefined4 *)(unaff_EBP + 0x18));
      *(undefined4 *)(unaff_EBP + -0x1c) = uVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      FUN_0056e8bd();
      uVar2 = FUN_0056e8c8();
      return uVar2;
    }
    uVar2 = 0;
  }
  else {
    uVar2 = *(undefined4 *)(unaff_EBP + -0x1c);
  }
  *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
  return uVar2;
}

