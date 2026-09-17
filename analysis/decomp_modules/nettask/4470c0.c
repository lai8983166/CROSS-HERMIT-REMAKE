
void FUN__text__004470c0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  undefined1 local_14;
  char local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    iVar1 = FUN__text__004128f0((&DAT_00605c00)[local_c * 2],1);
    if ((iVar1 != 0) || (iVar1 = FUN__text__004128f0((&DAT_00605c01)[local_c * 2],1), iVar1 != 0)) {
      if ((*(int *)(local_8 + 0x1bcc) % 3 != 0) || ((-1 < local_c && (local_c < 3)))) {
        *(undefined1 *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) = (undefined1)local_c;
        *(int *)(local_8 + 0x1bcc) = *(int *)(local_8 + 0x1bcc) + 1;
        if (0xb < *(int *)(local_8 + 0x1bcc)) {
          *(undefined4 *)(local_8 + 0x1bcc) = 0xb;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
      }
      goto LAB__text__0044763c;
    }
  }
  for (local_c = 0; local_c != 4; local_c = local_c + 1) {
    iVar1 = FUN__text__004128f0((&DAT_00605c14)[local_c],2);
    if (iVar1 != 0) {
      local_1c = local_c;
      switch(local_c) {
      case 0:
        *(int *)(local_8 + 0x1bcc) = *(int *)(local_8 + 0x1bcc) + -1;
        if (*(int *)(local_8 + 0x1bcc) < 0) {
          *(undefined4 *)(local_8 + 0x1bcc) = 0;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
        goto LAB__text__0044763c;
      case 1:
        *(int *)(local_8 + 0x1bcc) = *(int *)(local_8 + 0x1bcc) + 1;
        if (0xb < *(int *)(local_8 + 0x1bcc)) {
          *(undefined4 *)(local_8 + 0x1bcc) = 0xb;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
        goto LAB__text__0044763c;
      case 2:
        local_10 = '\t';
        if (*(int *)(local_8 + 0x1bcc) % 3 == 0) {
          local_10 = '\x02';
        }
        local_14 = 0;
        *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) =
             *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) + '\x01';
        if (local_10 < *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc))) {
          *(undefined1 *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) = 0;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
        goto LAB__text__0044763c;
      case 3:
        local_10 = '\t';
        if (*(int *)(local_8 + 0x1bcc) % 3 == 0) {
          local_10 = '\x02';
        }
        local_14 = 0;
        *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) =
             *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) + -1;
        if (*(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) < '\0') {
          *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) = local_10;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
        goto LAB__text__0044763c;
      }
    }
  }
  iVar1 = FUN__text__004128f0(0x1c,1);
  if (iVar1 == 0) {
    local_18 = FUN__text__0044c710(&DAT_00605c18,0xc);
    if ((local_18 == -1) || ((*(uint *)(DAT_007a49fc + 0x1990) & 1) == 0)) {
      if ((local_18 == -1) || ((*(uint *)(DAT_007a49fc + 0x1990) & 2) == 0)) {
        if (*(short *)(local_8 + 0x1bde) < 0x83) {
          *(short *)(local_8 + 0x1bde) =
               *(short *)(local_8 + 0x1bde) + (short)*(char *)(local_8 + 0x1bdc);
          if (*(short *)(local_8 + 0x1bde) < 100) {
            *(char *)(local_8 + 0x1bdc) = -*(char *)(local_8 + 0x1bdc);
          }
          if (0x7d < *(short *)(local_8 + 0x1bde)) {
            *(char *)(local_8 + 0x1bdc) = -*(char *)(local_8 + 0x1bdc);
          }
        }
        else {
          *(short *)(local_8 + 0x1bde) = *(short *)(local_8 + 0x1bde) + -10;
          *(undefined1 *)(local_8 + 0x1bdc) = 0xfe;
          if (*(short *)(local_8 + 0x1bde) < 0x96) {
            *(undefined2 *)(local_8 + 0x1bde) = 100;
          }
        }
      }
      else {
        *(int *)(local_8 + 0x1bcc) = local_18;
        local_10 = '\t';
        if (*(int *)(local_8 + 0x1bcc) % 3 == 0) {
          local_10 = '\x02';
        }
        local_14 = 0;
        *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) =
             *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) + -1;
        if (*(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) < '\0') {
          *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) = local_10;
        }
        *(undefined2 *)(local_8 + 0x1bde) = 0x118;
      }
    }
    else {
      *(int *)(local_8 + 0x1bcc) = local_18;
      local_10 = '\t';
      if (*(int *)(local_8 + 0x1bcc) % 3 == 0) {
        local_10 = '\x02';
      }
      local_14 = 0;
      *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) =
           *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) + '\x01';
      if (local_10 < *(char *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc))) {
        *(undefined1 *)(local_8 + 0x1bd0 + *(int *)(local_8 + 0x1bcc)) = 0;
      }
      *(undefined2 *)(local_8 + 0x1bde) = 0x118;
    }
  }
LAB__text__0044763c:
  local_8 = 0x447649;
  FUN__text__0056ce80();
  return;
}

