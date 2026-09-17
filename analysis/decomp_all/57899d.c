
undefined4 thunk_FUN_005789e2(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  iVar2 = (*API_KERNEL32_DLL_HeapValidate)(DAT_0080ab28,0,0);
  if (iVar2 == 0) {
    iVar2 = (*API_KERNEL32_DLL_GetLastError)();
    if (iVar2 == 0x78) {
      puVar3 = (undefined4 *)FUN_00576d30();
      *puVar3 = 0x78;
      puVar3 = (undefined4 *)FUN_00576d20();
      *puVar3 = 0x28;
    }
    else {
      *(undefined4 *)(unaff_EBP + -0x1c) = 0xfffffffc;
    }
  }
  uVar1 = *(undefined4 *)(unaff_EBP + -0x1c);
  *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
  return uVar1;
}

