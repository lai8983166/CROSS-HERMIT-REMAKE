
void __fastcall FUN_0040c140(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
    *(undefined2 *)(param_1 + 0x7094 + local_c * 4) = 0xffff;
    *(undefined2 *)(param_1 + 0x7096 + local_c * 4) = 0xffff;
  }
  return;
}

