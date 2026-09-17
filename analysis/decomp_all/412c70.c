
void FUN__text__00412c70(undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058ec6b;
  local_10 = ExceptionList;
  puVar2 = local_64;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  local_20 = FUN__text__00428a40(0xba20);
  local_8 = 0;
  if (local_20 == 0) {
    local_24 = 0;
  }
  else {
    local_24 = FUN__text__00412e30();
  }
  local_1c = local_24;
  local_8 = 0xffffffff;
  local_14 = local_24;
  if ((local_24 != 0) &&
     (local_18 = FUN__text__00413450(param_1,1,1,param_3,param_4), local_18 == 0)) {
    *param_2 = local_14;
  }
  ExceptionList = local_10;
  local_8 = 0x412d37;
  FUN__text__0056ce80();
  return;
}

