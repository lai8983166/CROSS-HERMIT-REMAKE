
int __thiscall FUN_00421e20(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [17];
  int *local_10;
  int local_c;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  do {
    if (local_c == 0x20) {
      return -1;
    }
    for (local_10 = (int *)(param_1 + local_c * 8); *local_10 != 0;
        local_10 = (int *)(*local_10 + 0xc)) {
      if (*local_10 == param_2) {
        return local_c;
      }
    }
    local_c = local_c + 1;
  } while( true );
}

