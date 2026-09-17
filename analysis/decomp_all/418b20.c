
void __fastcall FUN_00418b20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
    local_10 = local_8 + 0x250 + local_c * 0x54;
    if (*(int *)(local_10 + 0x30) != 0) {
      local_14 = *(undefined4 *)(local_10 + 0x30);
      FUN_00428ad0(local_14);
      *(undefined4 *)(local_10 + 0x30) = 0;
    }
    if (*(int *)(local_10 + 0x34) != 0) {
      local_18 = *(undefined4 *)(local_10 + 0x34);
      FUN_00428ad0(local_18);
      *(undefined4 *)(local_10 + 0x34) = 0;
    }
    if (*(int *)(local_10 + 0x50) != 0) {
      local_1c = *(undefined4 *)(local_10 + 0x50);
      FUN_00428ad0(local_1c);
      *(undefined4 *)(local_10 + 0x50) = 0;
    }
  }
  _memset((void *)(local_8 + 0x244),0,0x150c);
  local_8 = 0x418c0f;
  __chkesp();
  return;
}

