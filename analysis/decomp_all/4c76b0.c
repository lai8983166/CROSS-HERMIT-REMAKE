
undefined4 __thiscall FUN__text__004c76b0(undefined2 *param_1,undefined2 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  param_1[1] = param_2;
  *param_1 = 1;
  param_1[2] = 0;
  param_1[3] = 0x10;
  switch(param_1[1]) {
  case 2:
    *param_1 = 0;
    break;
  case 3:
    param_1[3] = 0x3c;
    break;
  case 4:
    param_1[3] = 0x3c;
    break;
  case 5:
    param_1[3] = 0x3c;
    break;
  case 6:
    param_1[3] = 0x3c;
  }
  return 1;
}

