
void FUN__text__0048e6d0(int param_1,int param_2)

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
    *(ushort *)(param_1 + 0x4ee) = (ushort)*(byte *)(param_2 + 2);
    *(undefined2 *)(param_1 + 0x4f2) = *(undefined2 *)(param_2 + 6);
    *(undefined1 *)(param_1 + 0x4f0) = *(undefined1 *)(param_2 + 3);
    *(undefined1 *)(param_1 + 0x4f1) = *(undefined1 *)(param_2 + 4);
    *(undefined1 *)(param_1 + 0x2a7) = 0;
    FUN__text__00475370(param_1,6,0xffffffff);
    FUN__text__0049ad90(param_1,0x6a);
  }
  local_8 = 0x48e77c;
  FUN__text__0056ce80();
  return;
}

