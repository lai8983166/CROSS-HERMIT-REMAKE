
void __fastcall FUN__text__00448920(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined1 local_1c;
  uint local_18;
  uint local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 4; local_c = local_c + 1) {
    *(undefined1 *)(param_1 + local_c + 0x1aac) = (undefined1)local_c;
  }
  local_8 = param_1;
  iVar1 = _rand();
  local_10 = iVar1 % 0x14 + 10;
  for (local_c = 0; local_c != local_10; local_c = local_c + 1) {
    local_14 = _rand();
    local_14 = local_14 & 0x80000003;
    if ((int)local_14 < 0) {
      local_14 = (local_14 - 1 | 0xfffffffc) + 1;
    }
    local_18 = local_14 + 1 & 0x80000003;
    if ((int)local_18 < 0) {
      local_18 = (local_18 - 1 | 0xfffffffc) + 1;
    }
    local_18 = _rand();
    local_18 = local_18 & 0x80000003;
    if ((int)local_18 < 0) {
      local_18 = (local_18 - 1 | 0xfffffffc) + 1;
    }
    local_1c = *(undefined1 *)(local_8 + local_14 + 0x1aac);
    *(undefined1 *)(local_8 + local_14 + 0x1aac) = *(undefined1 *)(local_8 + local_18 + 0x1aac);
    *(undefined1 *)(local_8 + local_18 + 0x1aac) = local_1c;
  }
  local_8 = 0x448a1f;
  FUN__text__0056ce80();
  return;
}

