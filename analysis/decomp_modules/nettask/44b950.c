
void __thiscall FUN__text__0044b950(int param_1,int param_2)

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
  if (param_2 == 0) {
    for (local_c = 0; local_c != 4; local_c = local_c + 1) {
      *(undefined1 *)(param_1 + local_c + 0x1a8c) = (undefined1)local_c;
    }
  }
  else {
    for (local_c = 0; local_c != 4; local_c = local_c + 1) {
      *(undefined1 *)(param_1 + local_c + 0x1a8c) = 0;
    }
  }
  return;
}

