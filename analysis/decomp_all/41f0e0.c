
void FUN__text__0041f0e0(undefined4 param_1,int param_2,int param_3,undefined4 param_4,int param_5,
                        int param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_78 [16];
  int *local_38;
  int *local_34;
  int *local_30;
  int local_2c;
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
  puStack_c = &LAB__text__0058ef3b;
  local_10 = ExceptionList;
  puVar3 = local_78;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = param_2;
  ExceptionList = &local_10;
  FUN__text__0041f4e0(param_3);
  local_2c = *(int *)(local_18 + 4);
  local_24 = local_2c;
  local_34 = (int *)FUN__text__00428a40(local_2c * 0x54 + 4);
  local_8 = 0;
  if (local_34 == (int *)0x0) {
    local_38 = (int *)0x0;
  }
  else {
    *local_34 = local_2c;
    _eh_vector_constructor_iterator_
              (local_34 + 1,0x54,local_2c,FUN__text__0041f830,FUN__text__0041f890);
    local_38 = local_34 + 1;
  }
  local_30 = local_38;
  local_8 = 0xffffffff;
  local_1c = local_38;
  if ((local_38 == (int *)0x0) &&
     (iVar2 = FUN__text__00424f80(&DAT_00594730,
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                                  DAT_005ff5d0 + 0x13,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_1c != (int *)0x0) {
    *(int **)(local_14 + param_3 * 8) = local_1c;
    *(int *)(local_14 + 4 + param_3 * 8) = local_24;
    for (local_20 = 0; local_20 != local_24; local_20 = local_20 + 1) {
      local_28 = 0;
      if (param_5 != 0) {
        if (param_6 == 0) {
          local_28 = param_5;
        }
        else if (*(char *)(param_6 + local_20) == '\0') {
          local_28 = param_5;
        }
      }
      iVar2 = FUN__text__0041f340(param_1,local_18,local_20,local_1c,param_4,local_28);
      if (iVar2 != 0) {
        FUN__text__0041f4e0(param_3);
        break;
      }
    }
  }
  ExceptionList = local_10;
  local_8 = 0x41f28c;
  FUN__text__0056ce80();
  return;
}

