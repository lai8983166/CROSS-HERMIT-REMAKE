
void FUN__text__0048e5d0(int param_1,int param_2)

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
  iVar1 = FUN__text__004693b0(param_1);
  if (iVar1 == 0) {
    *(ushort *)(param_1 + 0x4cc) = (ushort)*(byte *)(param_2 + 3) * 0x20 + 0x10;
    *(ushort *)(param_1 + 0x4ce) = (ushort)*(byte *)(param_2 + 4) * 0x10 + 8;
    *(undefined2 *)(param_1 + 0x4d0) = *(undefined2 *)(param_1 + 0x4cc);
    *(undefined2 *)(param_1 + 0x4d2) = *(undefined2 *)(param_1 + 0x4ce);
    *(undefined2 *)(param_1 + 0x4e0) = 0;
    *(undefined1 *)(param_1 + 0x2a7) = 0;
    FUN__text__00475370(param_1,4,0xffffffff);
    if (*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x01') {
      *(undefined1 *)(param_1 + 0x2e8) = *(undefined1 *)(param_2 + 3);
      *(undefined1 *)(param_1 + 0x2e9) = *(undefined1 *)(param_2 + 4);
    }
  }
  local_8 = 0x48e6c8;
  FUN__text__0056ce80();
  return;
}

