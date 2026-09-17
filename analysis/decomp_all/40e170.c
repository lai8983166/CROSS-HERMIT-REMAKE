
/* WARNING: Removing unreachable block (ram,0x0040e1c9) */

int * __thiscall FUN__text__0040e170(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int *local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x10) == 0) {
    local_c = (int *)0x0;
  }
  else {
    for (local_c = (int *)(*(int *)(param_1 + 0x10) + param_2 * 8); *local_c != 0;
        local_c = (int *)*local_c) {
    }
  }
  return local_c;
}

