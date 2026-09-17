
void FUN__text__004cbdb0(undefined4 param_1,undefined4 param_2,short param_3,short param_4,
                        undefined2 param_5,short param_6,short param_7,short param_8,short param_9,
                        undefined4 param_10,undefined4 param_11)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_d8 [16];
  undefined1 local_98;
  short local_5c;
  short local_5a;
  ushort local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  undefined1 local_2d;
  undefined2 local_1e;
  short local_1c;
  short local_1a;
  short local_18;
  short local_16;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0059060c;
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
  if (param_3 != -1) {
    local_38 = 1;
    local_2d = (undefined1)param_3;
  }
  if (param_4 != -1) {
    local_2e = (undefined1)param_4;
    local_2f = (undefined1)param_4;
    local_30 = (undefined1)param_4;
  }
  local_3c = local_3c | 0x40;
  local_34 = 0;
  local_1e = param_5;
  FUN__text__00407870(param_10,param_11);
  local_5c = param_8;
  local_5a = param_9;
  local_1c = param_6;
  local_1a = param_7;
  local_18 = param_6 + param_8;
  local_16 = param_7 + param_9;
  FUN__text__004079c0(param_1,param_2);
  local_98 = 1;
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x4cbef3;
  FUN__text__0056ce80();
  return;
}

