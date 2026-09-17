
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004406f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  uint local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _DAT_007a2970 = *(undefined4 *)(param_1 + 0x2646c);
  _DAT_007a2974 = *(undefined4 *)(param_1 + 0x26470);
  _DAT_007a2978 = *(undefined4 *)(param_1 + 0x26474);
  _DAT_007a297c = *(undefined4 *)(param_1 + 0x26478);
  DAT_007a2960 = *(int *)(param_1 + 0x2646c);
  DAT_007a2964 = *(int *)(param_1 + 0x26470);
  DAT_007a2968 = *(int *)(param_1 + 0x2646c) + *(int *)(param_1 + 0x26474);
  DAT_007a296c = *(int *)(param_1 + 0x26470) + *(int *)(param_1 + 0x26478);
  *(undefined4 *)(param_1 + 0x265e8) = 0;
  if (*(char *)(param_1 + 0x26597) == '\0') {
    local_c = (int)*(short *)(DAT_007a49fc + 0x196c);
    local_10 = (uint)*(short *)(DAT_007a49fc + 0x1970);
    if ((((DAT_007a2960 <= local_c) && (local_c < DAT_007a2968)) && (DAT_007a2964 <= (int)local_10))
       && (((int)local_10 < DAT_007a296c && (*(int *)(param_1 + 0x265d8) != 1)))) {
      local_8 = param_1;
      if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
        if (((*(uint *)(DAT_007a49fc + 0x1990) & 2) != 0) && (*(char *)(param_1 + 0x26596) == '\0'))
        {
          local_c = local_c - DAT_007a2960;
          local_10 = local_10 - DAT_007a2964;
          local_c = __ftol();
          local_10 = __ftol();
          if (local_c < 0) {
            local_c = 0;
          }
          if (*(short *)(*(int *)(local_8 + 0x2659c) + 4) * 0x20 <= local_c) {
            local_c = *(short *)(*(int *)(local_8 + 0x2659c) + 4) * 0x20 + -1;
          }
          if ((int)local_10 < 0) {
            local_10 = 0;
          }
          if (*(short *)(*(int *)(local_8 + 0x2659c) + 6) * 0x10 <= (int)local_10) {
            local_10 = *(short *)(*(int *)(local_8 + 0x2659c) + 6) * 0x10 - 1;
          }
          *(undefined4 *)(local_8 + 0x265e8) = 1;
          *(undefined2 *)(local_8 + 0x265ec) = (undefined2)local_c;
          *(undefined2 *)(local_8 + 0x265ee) = (undefined2)local_10;
        }
      }
      else {
        local_c = local_c - DAT_007a2960;
        local_10 = local_10 - DAT_007a2964;
        FUN__text__00440980(local_c,local_10 & 0xffff);
      }
    }
  }
  local_8 = 0x44096f;
  FUN__text__0056ce80();
  return;
}

