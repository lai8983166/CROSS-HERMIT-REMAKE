
void FUN__text__004cbca0(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined1 uStack00000018;
  undefined1 uStack0000001c;
  undefined2 in_stack_00000020;
  undefined2 in_stack_00000024;
  undefined4 in_stack_00000028;
  undefined4 in_stack_0000002c;
  undefined4 local_d8 [16];
  undefined1 local_98;
  undefined4 local_38;
  undefined4 local_34;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  undefined1 local_2d;
  undefined2 local_20;
  undefined2 local_1e;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005905ec;
  local_10 = ExceptionList;
  puVar2 = local_d8;
  for (iVar1 = 0x32; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__004077c0(DAT_007a49fc);
  if (_uStack00000018 != -1) {
    local_38 = 1;
    local_2d = uStack00000018;
  }
  if (_uStack0000001c != -1) {
    local_2e = uStack0000001c;
    local_2f = uStack0000001c;
    local_30 = uStack0000001c;
  }
  local_34 = 0;
  local_20 = in_stack_00000024;
  local_1e = in_stack_00000020;
  FUN__text__00407870(in_stack_00000028,in_stack_0000002c);
  FUN__text__004079c0(param_1,param_2);
  local_98 = 1;
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x4cbda8;
  FUN__text__0056ce80();
  return;
}

