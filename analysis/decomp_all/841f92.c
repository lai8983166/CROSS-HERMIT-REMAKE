
void FUN__text1__00841f92(int param_1,int param_2,int param_3,int param_4)

{
  uint local_10;
  uint local_c;
  int local_8;
  
  local_8 = 0;
  if (*(int *)(param_1 + 0x7c) < 1) {
    local_c = param_3 + 5;
    local_10 = local_c;
  }
  else {
    if (*(char *)(param_1 + 0x1c) == '\x02') {
      FUN__text1__0084484a(param_1);
    }
    FUN__text1__0084234e(param_1,param_1 + 0xb10);
    FUN__text1__0084234e(param_1,param_1 + 0xb1c);
    local_8 = FUN__text1__00842c85(param_1);
    local_10 = *(int *)(param_1 + 0x16a0) + 10U >> 3;
    local_c = *(int *)(param_1 + 0x16a4) + 10U >> 3;
    if (local_c <= local_10) {
      local_10 = local_c;
    }
  }
  if ((local_10 < param_3 + 4U) || (param_2 == 0)) {
    if (local_c == local_10) {
      if (*(int *)(param_1 + 0x16b4) < 0xe) {
        *(ushort *)(param_1 + 0x16b0) =
             *(ushort *)(param_1 + 0x16b0) |
             (ushort)(param_4 + 2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
      }
      else {
        *(ushort *)(param_1 + 0x16b0) =
             *(ushort *)(param_1 + 0x16b0) |
             (ushort)(param_4 + 2U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
             (char)*(undefined2 *)(param_1 + 0x16b0);
        *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
        *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
             (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
        *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
        *(short *)(param_1 + 0x16b0) =
             (short)((int)(param_4 + 2U & 0xffff) >>
                    (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
      }
      FUN__text1__00844002(param_1,&DAT_00873440,&DAT_008738c0);
    }
    else {
      if (*(int *)(param_1 + 0x16b4) < 0xe) {
        *(ushort *)(param_1 + 0x16b0) =
             *(ushort *)(param_1 + 0x16b0) |
             (ushort)(param_4 + 4 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
      }
      else {
        *(ushort *)(param_1 + 0x16b0) =
             *(ushort *)(param_1 + 0x16b0) |
             (ushort)(param_4 + 4U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
             (char)*(undefined2 *)(param_1 + 0x16b0);
        *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
        *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
             (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
        *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
        *(short *)(param_1 + 0x16b0) =
             (short)((int)(param_4 + 4U & 0xffff) >>
                    (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
        *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
      }
      FUN__text1__00842ed9
                (param_1,*(int *)(param_1 + 0xb14) + 1,*(int *)(param_1 + 0xb20) + 1,local_8 + 1);
      FUN__text1__00844002(param_1,param_1 + 0x8c,param_1 + 0x980);
    }
  }
  else {
    FUN__text1__00841964(param_1,param_2,param_3,param_4);
  }
  FUN__text1__0084189b(param_1);
  if (param_4 != 0) {
    FUN__text1__00844a26(param_1);
  }
  return;
}

