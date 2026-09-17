
void FUN__text__00420df0(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4
                        ,short param_5,undefined1 *param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_6 = 0x44;
  param_6[1] = 0x58;
  if (param_5 == 1) {
    *(undefined2 *)(param_6 + 2) = 1;
    *(undefined2 *)(param_6 + 4) = param_1;
    *(undefined2 *)(param_6 + 6) = param_2;
    *(undefined2 *)(param_6 + 8) = param_3;
    *(undefined2 *)(param_6 + 10) = param_4;
  }
  else if (param_5 == 2) {
    *(undefined2 *)(param_6 + 2) = 2;
    *(undefined2 *)(param_6 + 4) = param_1;
    *(undefined2 *)(param_6 + 6) = param_2;
    *(undefined2 *)(param_6 + 8) = param_3;
    *(undefined2 *)(param_6 + 10) = param_4;
  }
  else if (param_5 == 4) {
    *(undefined2 *)(param_6 + 2) = 4;
    *(undefined2 *)(param_6 + 4) = param_1;
    *(undefined2 *)(param_6 + 6) = param_2;
    *(undefined2 *)(param_6 + 8) = param_3;
    *(undefined2 *)(param_6 + 10) = param_4;
  }
  return;
}

