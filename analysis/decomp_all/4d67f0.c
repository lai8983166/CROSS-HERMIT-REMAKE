
void __thiscall
FUN__text__004d67f0(undefined1 *param_1,undefined1 param_2,undefined2 param_3,undefined2 param_4,
                   undefined2 param_5,undefined2 param_6,undefined2 param_7,undefined2 param_8,
                   undefined2 param_9,undefined2 param_10,undefined2 param_11)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined1 *local_c;
  undefined1 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = param_2;
  *(undefined2 *)(param_1 + 2) = param_4;
  *(undefined2 *)(param_1 + 4) = 1;
  *(undefined2 *)(param_1 + 6) = param_7;
  *(undefined2 *)(param_1 + 8) = param_8;
  *(undefined2 *)(param_1 + 0xe) = param_9;
  *(undefined2 *)(param_1 + 0x10) = param_10;
  *(undefined2 *)(param_1 + 0x1a) = param_11;
  *(undefined2 *)(param_1 + 0x1e) = param_5;
  *(undefined2 *)(param_1 + 0x20) = param_6;
  *(undefined2 *)(param_1 + 0x22) = param_3;
  local_c = param_1;
  local_8 = param_1;
  FUN__text__004d6930(param_1);
  local_8 = (undefined1 *)0x4d68a0;
  FUN__text__0056ce80();
  return;
}

