
void FUN__text__004de930(int param_1,undefined2 *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_2,0,0x2c);
  *param_2 = *(undefined2 *)(*(int *)(param_1 + 600) + 0x3a);
  param_2[1] = *(undefined2 *)(*(int *)(param_1 + 600) + 0x3c);
  param_2[2] = *(undefined2 *)(*(int *)(param_1 + 600) + 0x38);
  *(undefined1 *)(param_2 + 4) = *(undefined1 *)(*(int *)(param_1 + 600) + 0x4c);
  *(undefined1 *)((int)param_2 + 9) = *(undefined1 *)(*(int *)(param_1 + 600) + 0x4d);
  *(undefined1 *)(param_2 + 5) = *(undefined1 *)(*(int *)(param_1 + 600) + 0x50);
  *(undefined1 *)((int)param_2 + 0xb) = *(undefined1 *)(*(int *)(param_1 + 600) + 0x4f);
  *(undefined1 *)(param_2 + 6) = *(undefined1 *)(*(int *)(param_1 + 600) + 0x4e);
  param_2[0x12] = *(undefined2 *)(*(int *)(param_1 + 600) + 0x52);
  *(undefined4 *)(param_2 + 0xe) = 0;
  *(undefined4 *)(param_2 + 0x10) = 0;
  uStack_8 = 0x4dea22;
  FUN__text__0056ce80();
  return;
}

