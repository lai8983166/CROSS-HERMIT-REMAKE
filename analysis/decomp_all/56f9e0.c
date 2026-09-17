
void FUN__text__0056f9e0(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9980;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  ExceptionList = &pvStack_14;
  FUN__text__00577040(9);
  local_8 = 0;
  iVar2 = FUN__text__00570050(param_1);
  if (iVar2 != 0) {
    if (((((*(uint *)(param_1 + -0xc) & 0xffff) != 4) && (*(int *)(param_1 + -0xc) != 1)) &&
        ((*(uint *)(param_1 + -0xc) & 0xffff) != 2)) &&
       ((*(int *)(param_1 + -0xc) != 3 &&
        (iVar2 = FUN__text__00573780(2,"dbgheap.c",0x4ff,0,"_BLOCK_TYPE_IS_VALID(pHead->nBlockUse)")
        , iVar2 == 1)))) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined4 *)(param_1 + -0xc) = param_2;
  }
  local_8 = 0xffffffff;
  FUN__text__0056fa9d();
  FUN__text__0056faa8();
  return;
}

