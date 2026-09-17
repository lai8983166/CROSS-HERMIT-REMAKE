
void FUN__text__00574d80(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar1;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa048;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  ExceptionList = &pvStack_14;
  FUN__text__005753b0();
  FUN__text__005753b0();
  iVar1 = FUN__text__005753b0();
  *(undefined4 *)(iVar1 + 0x6c) = param_1;
  iVar1 = FUN__text__005753b0();
  *(undefined4 *)(iVar1 + 0x70) = param_3;
  local_8 = 1;
  FUN__text__0056d140(param_2,param_4,param_5,param_6,param_7);
  local_8 = 0xffffffff;
  FUN__text__00574e5d();
  FUN__text__00574ebb();
  return;
}

