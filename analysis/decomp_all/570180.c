
/* Library Function - Single Match
    __CrtIsMemoryBlock
   
   Library: Visual Studio 2003 Debug */

undefined4
__CrtIsMemoryBlock(int param_1,int param_2,undefined4 *param_3,undefined4 *param_4,
                  undefined4 *param_5)

{
  int iVar1;
  undefined4 uVar2;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9b28;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  ExceptionList = &pvStack_14;
  iVar1 = FUN__text__00570050(param_1);
  if (iVar1 != 0) {
    FUN__text__00577040(9);
    local_8 = 0;
    if ((((((*(uint *)(param_1 + -0xc) & 0xffff) == 4) || (*(int *)(param_1 + -0xc) == 1)) ||
         ((*(uint *)(param_1 + -0xc) & 0xffff) == 2)) || (*(int *)(param_1 + -0xc) == 3)) &&
       (((iVar1 = __CrtIsValidPointer(param_1,param_2,1), iVar1 != 0 &&
         (*(int *)(param_1 + -0x10) == param_2)) && (*(int *)(param_1 + -8) <= DAT_007619c4)))) {
      if (param_3 != (undefined4 *)0x0) {
        *param_3 = *(undefined4 *)(param_1 + -8);
      }
      if (param_4 != (undefined4 *)0x0) {
        *param_4 = *(undefined4 *)(param_1 + -0x18);
      }
      if (param_5 != (undefined4 *)0x0) {
        *param_5 = *(undefined4 *)(param_1 + -0x14);
      }
    }
    local_8 = 0xffffffff;
    FUN__text__00570286();
    uVar2 = FUN__text__00570291();
    return uVar2;
  }
  ExceptionList = pvStack_14;
  return 0;
}

