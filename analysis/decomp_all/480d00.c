
void FUN__text__00480d00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_7c [16];
  undefined1 local_3c;
  char local_38;
  char local_34 [16];
  undefined1 local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_7c;
  for (iVar1 = 0x1e; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(local_34,0,0x10);
  local_14 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                          (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_18 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_c = (int *)(local_8 + 0xdc8ec);
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    if ((*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4) != '\a') &&
       (*(short *)(param_1 + 2) != *(short *)(local_c[local_10 + 1] + 2))) {
      local_1c = (short)((int)((*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x10) +
                              (*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_20 = (short)((int)((*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x10) +
                              (*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      local_24 = 5;
      iVar1 = FUN__text__0043c1d0((int)local_14,(int)local_18,(int)local_1c,(int)local_20,5);
      if (iVar1 != 0) {
        local_34[*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4)] =
             local_34[*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4)] + '\x01';
      }
    }
  }
  local_38 = '\0';
  local_3c = 0xff;
  for (local_10 = 0xf; -1 < local_10; local_10 = local_10 + -1) {
    if (local_38 < local_34[local_10]) {
      local_38 = local_34[local_10];
      local_3c = (undefined1)local_10;
    }
  }
  local_8 = 0x480f3b;
  FUN__text__0056ce80();
  return;
}

