
void FUN__text__0056ff50(code *param_1,undefined4 param_2)

{
  undefined4 *local_20;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9b18;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  if ((DAT_007619c0 & 1) == 0) {
    ExceptionList = &pvStack_14;
    FUN__text__0056ffe8();
    return;
  }
  ExceptionList = &pvStack_14;
  FUN__text__00577040(9);
  local_8 = 0;
  for (local_20 = DAT_0080a438; local_20 != (undefined4 *)0x0; local_20 = (undefined4 *)*local_20) {
    if ((local_20[5] & 0xffff) == 4) {
      (*param_1)(local_20 + 8,param_2);
    }
  }
  local_8 = 0xffffffff;
  FUN__text__0056ffdd();
  FUN__text__0056ffe8();
  return;
}

