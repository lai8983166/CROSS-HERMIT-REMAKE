
undefined4 __fastcall FUN__text__00446fa0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  short local_10 [4];
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_10[0] = *(char *)(param_1 + 0x1bd0) * 100 + *(char *)(param_1 + 0x1bd1) * 10 +
                (short)*(char *)(param_1 + 0x1bd2);
  local_10[1] = *(char *)(param_1 + 0x1bd3) * 100 + *(char *)(param_1 + 0x1bd4) * 10 +
                (short)*(char *)(param_1 + 0x1bd5);
  local_10[2] = *(char *)(param_1 + 0x1bd6) * 100 + *(char *)(param_1 + 0x1bd7) * 10 +
                (short)*(char *)(param_1 + 0x1bd8);
  local_10[3] = *(char *)(param_1 + 0x1bd9) * 100 + *(char *)(param_1 + 0x1bda) * 10 +
                (short)*(char *)(param_1 + 0x1bdb);
  local_14 = 0;
  while( true ) {
    if (local_14 == 4) {
      return 1;
    }
    if (0xff < local_10[local_14]) break;
    if (local_10[local_14] < 0) {
      return 0;
    }
    local_14 = local_14 + 1;
  }
  return 0;
}

