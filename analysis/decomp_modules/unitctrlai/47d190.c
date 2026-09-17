
void FUN__text__0047d190(int param_1,short param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(short *)(param_1 + 0x4cc) = param_2 * 0x20 + 0x10;
  *(short *)(param_1 + 0x4ce) = param_3 * 0x10 + 8;
  *(undefined2 *)(param_1 + 0x4d0) = *(undefined2 *)(param_1 + 0x4cc);
  *(undefined2 *)(param_1 + 0x4d2) = *(undefined2 *)(param_1 + 0x4ce);
  return;
}

