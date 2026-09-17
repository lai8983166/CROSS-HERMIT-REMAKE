
void FUN__text__00468810(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00468d80(param_1);
  if (iVar1 != 0) {
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x2c) = 0x1f;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x2e) = 200;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x37) = 0x1f;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x38) = 999;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x3a) = 200;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x3c) = 100;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x18) = 1;
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x1e) = 1;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x4c) = 0xff;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x4d) = 0xff;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x4e) = 0xff;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x4f) = 0xff;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x50) = 0xff;
  }
  local_8 = 0x468904;
  FUN__text__0056ce80();
  return;
}

