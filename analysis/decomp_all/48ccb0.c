
undefined4 FUN__text__0048ccb0(int param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == 10) {
    if (*(byte *)(*(int *)(param_1 + 600) + 5) < 0x4b) {
      param_3 = 0x1f;
    }
    else {
      param_3 = 0x20;
    }
  }
  else if (param_2 == 0x10) {
    if (*(byte *)(*(int *)(param_1 + 600) + 5) < 0x4b) {
      param_3 = 0x20;
    }
    else {
      param_3 = 0x21;
    }
  }
  return param_3;
}

