
void __fastcall FUN__text__0043c700(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  uint local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(int *)(param_1 + 0x2659c) != 0) && (*(char *)(param_1 + 0x26595) == '\0')) {
    *(undefined2 *)(param_1 + 0x265b2) = 8;
    *(undefined2 *)(param_1 + 0x265b4) = 8;
    if (*(int *)(DAT_007a49fc + 0x198c) == 0) {
      local_10 = 0;
      local_c = 0;
      local_8 = param_1;
      local_14 = FUN__text__0043c920();
      if ((local_14 & 1) != 0) {
        local_10 = *(short *)(local_8 + 0x265b4) * -2;
      }
      if ((local_14 & 2) != 0) {
        local_10 = *(short *)(local_8 + 0x265b4) << 1;
      }
      if ((local_14 & 4) != 0) {
        local_c = *(short *)(local_8 + 0x265b2) * -2;
      }
      if ((local_14 & 8) != 0) {
        local_c = *(short *)(local_8 + 0x265b2) << 1;
      }
      local_c = FUN__text__00415040((int)local_c);
      local_10 = FUN__text__00415040((int)local_10);
      *(short *)(local_8 + 0x265a6) = *(short *)(local_8 + 0x265a6) + local_c;
      *(short *)(local_8 + 0x265a8) = *(short *)(local_8 + 0x265a8) + local_10;
      if (*(short *)(local_8 + 0x265a6) < 0) {
        *(undefined2 *)(local_8 + 0x265a6) = 0;
      }
      if (*(short *)(*(int *)(local_8 + 0x2659c) + 4) * 0x20 + -0x400 <=
          (int)*(short *)(local_8 + 0x265a6)) {
        *(short *)(local_8 + 0x265a6) = *(short *)(*(int *)(local_8 + 0x2659c) + 4) * 0x20 + -0x400;
      }
      if (*(short *)(local_8 + 0x265a8) < 0) {
        *(undefined2 *)(local_8 + 0x265a8) = 0;
      }
      if (*(short *)(*(int *)(local_8 + 0x2659c) + 6) * 0x10 + -0x238 <=
          (int)*(short *)(local_8 + 0x265a8)) {
        *(short *)(local_8 + 0x265a8) = *(short *)(*(int *)(local_8 + 0x2659c) + 6) * 0x10 + -0x238;
      }
    }
  }
  local_8 = 0x43c913;
  FUN__text__0056ce80();
  return;
}

