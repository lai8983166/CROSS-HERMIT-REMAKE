
void FUN__text__00575580(void)

{
  int iVar1;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_005fa088;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  local_8 = 0;
  ExceptionList = &pvStack_14;
  iVar1 = FUN__text__005753b0();
  if (*(int *)(iVar1 + 0x60) != 0) {
    local_8 = 1;
    iVar1 = FUN__text__005753b0();
    (**(code **)(iVar1 + 0x60))();
  }
  local_8 = 0xffffffff;
                    /* WARNING: Subroutine does not return */
  _abort();
}

