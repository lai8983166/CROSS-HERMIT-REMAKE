
void FUN__text__00490cd0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  char local_24;
  char local_20;
  char local_1c;
  char local_18;
  int local_14;
  int local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0046c9f0(param_2);
  if (iVar1 == 0) {
    local_1c = *(char *)(param_1 + 0x14);
    if (local_1c == '\t') {
      local_c = &DAT_006c2dc8 + param_2 * 0x48;
      if ((&DAT_006c2dcd)[param_2 * 0x48] == '\x01') {
        local_10._0_2_ = (undefined2)((*(short *)(param_1 + 0xe) * 0x96) / 100);
        *(undefined2 *)(param_1 + 0xe) = (undefined2)local_10;
        local_10 = (*(short *)(param_1 + 0x12) * 0x96) / 100;
        *(undefined2 *)(param_1 + 0x12) = (undefined2)local_10;
      }
      goto LAB__text__00490f7c;
    }
    if (local_1c == '\n') {
      local_c = &DAT_006c2dc8 + param_2 * 0x48;
      if ((&DAT_006c2dcd)[param_2 * 0x48] == '\x02') {
        local_10._0_2_ = (undefined2)((*(short *)(param_1 + 0xe) * 0x96) / 100);
        *(undefined2 *)(param_1 + 0xe) = (undefined2)local_10;
        local_10 = (*(short *)(param_1 + 0x12) * 0x96) / 100;
        *(undefined2 *)(param_1 + 0x12) = (undefined2)local_10;
      }
      goto LAB__text__00490f7c;
    }
  }
  else {
    local_18 = *(char *)(param_1 + 0x14);
    if (local_18 == '\a') {
      local_10._0_2_ = (undefined2)((*(short *)(param_1 + 0xe) * 0x96) / 100);
      *(undefined2 *)(param_1 + 0xe) = (undefined2)local_10;
      local_10 = (*(short *)(param_1 + 0x12) * 0x96) / 100;
      *(undefined2 *)(param_1 + 0x12) = (undefined2)local_10;
      goto LAB__text__00490f7c;
    }
  }
  local_20 = *(char *)(param_1 + 0x14);
  if (local_20 == '\r') {
    iVar1 = (uint)*(ushort *)(param_1 + 0x18) * 0x48;
    local_c = &DAT_006c2dc8 + iVar1;
    local_14 = (int)*(short *)(&DAT_006c2dec + iVar1) +
               (int)((uint)*(byte *)(*(int *)(param_1 + 600) + 7) *
                    (int)*(short *)(&DAT_006c2dee + iVar1)) / 100;
    local_10._0_2_ = (undefined2)((*(short *)(param_1 + 0xe) * local_14) / 100);
    *(undefined2 *)(param_1 + 0xe) = (undefined2)local_10;
    local_10 = (*(short *)(param_1 + 0x12) * local_14) / 100;
    *(undefined2 *)(param_1 + 0x12) = (undefined2)local_10;
  }
  else {
    local_24 = *(char *)(param_1 + 0x34);
    if (local_24 == '4') {
      iVar1 = (uint)*(ushort *)(param_1 + 0x38) * 0x48;
      local_c = &DAT_006c2dc8 + iVar1;
      local_14 = (int)*(short *)(&DAT_006c2dec + iVar1) +
                 (int)((uint)*(byte *)(*(int *)(param_1 + 600) + 7) *
                      (int)*(short *)(&DAT_006c2dee + iVar1)) / 100;
      local_10._0_2_ = (undefined2)((*(short *)(param_1 + 0xe) * local_14) / 100);
      *(undefined2 *)(param_1 + 0xe) = (undefined2)local_10;
      local_10 = (*(short *)(param_1 + 0x12) * local_14) / 100;
      *(undefined2 *)(param_1 + 0x12) = (undefined2)local_10;
    }
  }
LAB__text__00490f7c:
  local_8 = 0x490f89;
  FUN__text__0056ce80();
  return;
}

