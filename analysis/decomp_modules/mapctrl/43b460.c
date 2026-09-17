
void __thiscall FUN__text__0043b460(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 < 0) {
    param_2 = 0;
  }
  if (*(short *)(*(int *)(param_1 + 0x2659c) + 4) * 0x20 + -0x400 <= param_2) {
    param_2 = *(short *)(*(int *)(param_1 + 0x2659c) + 4) * 0x20 + -0x400;
  }
  if (param_3 < 0) {
    param_3 = 0;
  }
  if (*(short *)(*(int *)(param_1 + 0x2659c) + 6) * 0x10 + -0x238 <= param_3) {
    param_3 = *(short *)(*(int *)(param_1 + 0x2659c) + 6) * 0x10 + -0x238;
  }
  *(undefined2 *)(param_1 + 0x265a6) = (undefined2)param_2;
  *(undefined2 *)(param_1 + 0x265a8) = (undefined2)param_3;
  return;
}

