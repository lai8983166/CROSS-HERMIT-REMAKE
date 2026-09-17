
void FUN__text__004251e0(undefined4 param_1,short param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  int *local_28;
  int *local_24;
  int *local_20;
  int local_1c;
  int local_18;
  short *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058ef9b;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004251a0();
  *local_14 = param_2;
  local_1c = (int)*local_14;
  local_24 = (int *)FUN__text__00428a40(local_1c * 0x8c + 4);
  local_8 = 0;
  if (local_24 == (int *)0x0) {
    local_28 = (int *)0x0;
  }
  else {
    *local_24 = local_1c;
    _eh_vector_constructor_iterator_
              (local_24 + 1,0x8c,local_1c,FUN__text__00409300,FUN__text__00409360);
    local_28 = local_24 + 1;
  }
  local_20 = local_28;
  local_8 = 0xffffffff;
  *(int **)(local_14 + 4) = local_28;
  if ((*(int *)(local_14 + 4) == 0) &&
     (iVar2 = FUN__text__00424f80("SpFont!=0","e:\\crosshermit\\game\\src\\system\\syschatbox.cpp",
                                  DAT_005ff614 + 9,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_14 + 4) != 0) {
    for (local_18 = 0; local_18 != *local_14; local_18 = local_18 + 1) {
      FUN__text__004077c0(param_1);
      FUN__text__00409480(param_3);
      FUN__text__004094c0(0);
    }
    local_14[1] = 0;
    local_14[2] = 0;
  }
  ExceptionList = local_10;
  local_8 = 0x425374;
  FUN__text__0056ce80();
  return;
}

