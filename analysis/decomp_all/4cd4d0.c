
void FUN__text__004cd4d0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (uint)*(ushort *)(param_1 + 2);
  if (local_c == 1) {
    if (*(short *)(param_1 + 4) != *(short *)(param_1 + 2)) {
      FUN__text__004cade0();
    }
  }
  else if (local_c == 2) {
    FUN__text__004cb220(*(undefined2 *)(param_1 + 0x1e),*(undefined2 *)(param_1 + 0x20));
  }
  *(undefined2 *)(param_1 + 4) = *(undefined2 *)(param_1 + 2);
  local_8 = 0x4cd55e;
  FUN__text__0056ce80();
  return;
}

