
undefined4 __thiscall FUN__text__0043d530(int param_1,short param_2,short param_3)

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
  local_c = 0;
  while( true ) {
    if (local_c == *(int *)(param_1 + 0x263c8)) {
      return 0;
    }
    if ((*(short *)(param_1 + 0x263cc + local_c * 4) == param_2) &&
       (*(short *)(param_1 + 0x263ce + local_c * 4) == param_3)) break;
    local_c = local_c + 1;
  }
  return 1;
}

