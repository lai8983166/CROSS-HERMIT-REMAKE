
void __fastcall FUN__text__00499910(int param_1)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined *local_10;
  char *local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = (char *)(param_1 + 0x30998);
  iVar3 = *(char *)(param_1 + 0x3099a) * 0xe;
  local_10 = &DAT_0059eaa4 + iVar3;
  local_14 = 0;
  *(undefined2 *)(param_1 + 0x309a8) = *(undefined2 *)(&DAT_0059eaac + iVar3);
  *(undefined2 *)(param_1 + 0x309aa) = *(undefined2 *)(&DAT_0059eaae + iVar3);
  if (*local_c != '\0') {
    local_18 = (int)*(char *)(param_1 + 0x30999);
    local_8 = param_1;
    switch(local_18) {
    case 0:
      *(undefined4 *)(param_1 + 0x309a0) = 0;
      uVar2 = FUN__text__00415040((int)*(short *)(&DAT_0059eaa6 + iVar3));
      *(undefined4 *)(local_c + 0xc) = uVar2;
      local_c[1] = local_c[1] + '\x01';
    case 1:
      *(int *)(local_c + 8) = *(int *)(local_c + 8) + *(int *)(local_c + 0xc);
      if (0xfeff < *(int *)(local_c + 8)) {
        local_c[8] = '\0';
        local_c[9] = -1;
        local_c[10] = '\0';
        local_c[0xb] = '\0';
        if ((*(short *)(local_10 + 0xc) == 0) || (iVar3 = FUN__text__00456b20(), iVar3 != 0)) {
          uVar1 = FUN__text__00415070((int)*(short *)(local_10 + 4));
          *(undefined2 *)(local_c + 4) = uVar1;
          local_c[1] = '\x03';
        }
        else {
          local_c[1] = local_c[1] + '\x01';
        }
      }
      break;
    case 2:
      if (((*(uint *)(DAT_007a49fc + 0x1990) & 1) != 0) ||
         ((*(uint *)(DAT_007a49fc + 0x1950) & 0x8000) != 0)) {
        if (*(char *)(param_1 + 0x3099a) == '\0') {
          FUN__text__0049ad50(0);
        }
        else {
          FUN__text__0049ad50(5);
        }
        local_c[1] = '\x04';
        uVar2 = FUN__text__00415040((int)*(short *)(local_10 + 6));
        *(undefined4 *)(local_c + 0xc) = uVar2;
      }
      break;
    case 3:
      *(short *)(param_1 + 0x3099c) = *(short *)(param_1 + 0x3099c) + -1;
      if (*(short *)(param_1 + 0x3099c) == 0) {
        *(undefined1 *)(param_1 + 0x30999) = 4;
        uVar2 = FUN__text__00415040((int)*(short *)(&DAT_0059eaaa + iVar3));
        *(undefined4 *)(local_c + 0xc) = uVar2;
      }
      break;
    case 4:
      *(int *)(param_1 + 0x309a0) = *(int *)(param_1 + 0x309a0) - *(int *)(param_1 + 0x309a4);
      if (*(int *)(param_1 + 0x309a0) < 0x100) {
        *(undefined4 *)(param_1 + 0x309a0) = 0;
        *(char *)(param_1 + 0x30999) = *(char *)(param_1 + 0x30999) + '\x01';
      }
      break;
    case 5:
      *local_c = '\0';
      local_14 = 1;
    }
  }
  local_8 = 0x499b59;
  FUN__text__0056ce80();
  return;
}

