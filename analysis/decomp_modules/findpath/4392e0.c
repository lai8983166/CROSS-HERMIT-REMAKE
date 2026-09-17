
undefined4 __fastcall FUN__text__004392e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(int *)(param_1 + 0x28);
  do {
    if (local_c == 0) {
      return 0;
    }
    for (local_10 = *(int *)(param_1 + 0x34); local_10 != 0; local_10 = *(int *)(local_10 + 4)) {
      if (local_c == local_10) {
        return 1;
      }
    }
    local_c = *(int *)(local_c + 4);
  } while( true );
}

