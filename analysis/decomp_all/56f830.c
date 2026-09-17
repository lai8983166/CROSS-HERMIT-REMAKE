
void FUN_0056f830(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9970;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  if ((((DAT_007619c0 & 4) != 0) && (iVar2 = FUN_0056fb70(), iVar2 == 0)) &&
     (iVar2 = FUN_00573780(2,"dbgheap.c",0x49d,0,"_CrtCheckMemory()"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN_00577040(9);
  local_8 = 0;
  iVar2 = FUN_00570050(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN_00573780(2,"dbgheap.c",0x4a9,0,"_CrtIsValidHeapPointer(pUserData)"), iVar2 == 1))
  {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((((*(uint *)(param_1 + -0xc) & 0xffff) != 4) && (*(int *)(param_1 + -0xc) != 1)) &&
     (((*(uint *)(param_1 + -0xc) & 0xffff) != 2 &&
      ((*(int *)(param_1 + -0xc) != 3 &&
       (iVar2 = FUN_00573780(2,"dbgheap.c",0x4af,0,"_BLOCK_TYPE_IS_VALID(pHead->nBlockUse)"),
       iVar2 == 1)))))) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(param_1 + -0xc) == 2) && (param_2 == 1)) {
    param_2 = 2;
  }
  if (((*(int *)(param_1 + -0xc) != 3) && (*(int *)(param_1 + -0xc) != param_2)) &&
     (iVar2 = FUN_00573780(2,"dbgheap.c",0x4b6,0,"pHead->nBlockUse == nBlockUse"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0xffffffff;
  FUN_0056f9a1();
  FUN_0056f9ac();
  return;
}

