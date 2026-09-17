
void FUN__text__004176e0(undefined4 param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_7c [16];
  int *local_3c;
  int *local_38;
  int *local_34;
  int local_30;
  undefined4 local_2c;
  int local_28;
  int local_24;
  int local_20;
  int *local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058eecb;
  local_10 = ExceptionList;
  puVar2 = local_7c;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = param_2;
  ExceptionList = &local_10;
  FUN__text__00417950(param_3);
  local_30 = *(int *)(local_18 + 4);
  local_24 = local_30;
  local_38 = (int *)FUN__text__00428a40(local_30 * 0x10 + 4);
  local_8 = 0;
  if (local_38 == (int *)0x0) {
    local_3c = (int *)0x0;
  }
  else {
    *local_38 = local_30;
    _eh_vector_constructor_iterator_
              (local_38 + 1,0x10,local_30,FUN__text__00417b80,FUN__text__00417bd0);
    local_3c = local_38 + 1;
  }
  local_34 = local_3c;
  local_8 = 0xffffffff;
  local_1c = local_3c;
  if (local_3c != (int *)0x0) {
    *(int **)(local_14 + param_3 * 8) = local_3c;
    *(int *)(local_14 + 4 + param_3 * 8) = local_24;
    for (local_20 = 0; local_20 != local_24; local_20 = local_20 + 1) {
      local_2c = FUN__text__004214f0(local_18,local_20);
      local_28 = FUN__text__00417a70(param_1,local_1c + local_20 * 4,local_2c);
      if (local_28 != 0) {
        FUN__text__00417950(param_3);
        break;
      }
    }
  }
  ExceptionList = local_10;
  local_8 = 0x417847;
  FUN__text__0056ce80();
  return;
}

