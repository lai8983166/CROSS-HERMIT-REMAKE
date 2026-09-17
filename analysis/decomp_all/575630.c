
void FUN__text__00575630(void)

{
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_005fa0a0;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  ExceptionList = &pvStack_14;
  if (PTR_DAT_00761bc4 != (undefined *)0x0) {
    local_8 = 1;
    ExceptionList = &pvStack_14;
    (*(code *)PTR_DAT_00761bc4)();
  }
  local_8 = 0xffffffff;
  FUN__text__0057569a();
  FUN__text__005756a0();
  return;
}

