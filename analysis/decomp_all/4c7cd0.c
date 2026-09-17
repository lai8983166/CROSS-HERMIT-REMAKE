
void FUN__text__004c7cd0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004cade0();
  if (*(char *)(local_8 + 0x1a08) == '\0') {
    *(undefined1 *)(local_8 + 0x1a09) = 4;
  }
  else {
    *(undefined1 *)(local_8 + 0x1a09) = 1;
  }
  *(undefined **)(local_8 + 0x1a0c) = &DAT_00624520 + (uint)*(byte *)(local_8 + 0x1a09) * 0x26;
  *(undefined2 *)(local_8 + 0x14) = *(undefined2 *)(*(int *)(local_8 + 0x1a0c) + 0xe);
  *(short *)(local_8 + 0x16) = *(short *)(*(int *)(local_8 + 0x1a0c) + 0x10) + -8;
  if (DAT_007df1aa == 2) {
    *(undefined2 *)(local_8 + 10) = 0;
    *(undefined2 *)(local_8 + 8) = 7;
    *(undefined1 *)(local_8 + 0x1a0a) = 0;
    *(undefined2 *)(local_8 + 0xe) = 0;
    local_c = (uint)local_c._2_2_ << 0x10;
    while ((local_c & 0xffff) < 10) {
      *(undefined2 *)(local_8 + 0x2a + (local_c & 0xffff) * 0x298) = 0;
      *(undefined2 *)(local_8 + 0x24 + (local_c & 0xffff) * 0x298) = 0;
      *(undefined2 *)(local_8 + 0x26 + (local_c & 0xffff) * 0x298) = 0x10;
      *(undefined2 *)(local_8 + 0x28 + (local_c & 0xffff) * 0x298) = 0x10;
      *(undefined2 *)(local_8 + 0x22 + (local_c & 0xffff) * 0x298) = 0;
      *(undefined2 *)(local_8 + 0x18 + (local_c & 0xffff) * 0x298) = 3;
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
  }
  else {
    *(undefined2 *)(local_8 + 10) = 0;
    *(undefined2 *)(local_8 + 8) = 1;
    *(undefined1 *)(local_8 + 0x1a0a) = 1;
    *(undefined2 *)(local_8 + 0xe) = 0;
    *(undefined2 *)(local_8 + 0xc) = 0;
    *(undefined2 *)(local_8 + 0x10) = 0x10;
    *(undefined2 *)(local_8 + 0x12) = 0x10;
    local_c = (uint)local_c._2_2_ << 0x10;
    while ((local_c & 0xffff) < 10) {
      *(undefined2 *)(local_8 + 0x18 + (local_c & 0xffff) * 0x298) = 1;
      *(undefined2 *)(local_8 + 0x2a + (local_c & 0xffff) * 0x298) = 0;
      *(undefined2 *)(local_8 + 0x24 + (local_c & 0xffff) * 0x298) = 0;
      *(undefined2 *)(local_8 + 0x22 + (local_c & 0xffff) * 0x298) = 0x10;
      *(undefined2 *)(local_8 + 0x26 + (local_c & 0xffff) * 0x298) = 0x10;
      *(undefined2 *)(local_8 + 0x28 + (local_c & 0xffff) * 0x298) = 0x10;
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
  }
  local_8 = 0x4c7f72;
  FUN__text__0056ce80();
  return;
}

