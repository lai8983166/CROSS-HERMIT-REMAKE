
void FUN__text__00504f10(undefined2 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        )

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_d4 [38];
  undefined2 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  undefined1 local_2d;
  undefined2 local_24;
  undefined2 local_22;
  undefined2 local_20;
  undefined2 local_1e;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__00590b0c;
  local_10 = ExceptionList;
  puVar2 = local_d4;
  for (iVar1 = 0x31; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__004077c0(DAT_007a49fc);
  local_3c = 0;
  local_24 = 100;
  local_22 = 100;
  local_20 = 0;
  local_34 = 0;
  local_38 = 1;
  local_2d = 0xff;
  local_2e = 0x80;
  local_2f = 0x80;
  local_30 = 0x80;
  local_1e = param_1;
  FUN__text__00407870(10,param_2);
  FUN__text__004079c0(param_3,param_4);
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x504ff9;
  FUN__text__0056ce80();
  return;
}

