
void __fastcall FUN__text__004563d0(int param_1)

{
  code *pcVar1;
  undefined2 uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_58 [16];
  int local_18;
  char local_14;
  char *local_10;
  undefined *local_c;
  int local_8;
  
  puVar5 = local_58;
  for (iVar4 = 0x15; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  iVar4 = *(int *)(param_1 + 0x60);
  local_10 = (char *)(iVar4 + 0x2434);
  if (*local_10 != '\0') {
    local_14 = *(char *)(iVar4 + 0x2435);
    local_8 = param_1;
    if (local_14 == '\0') {
      local_c = &DAT_0060cabc;
      *(undefined2 *)(iVar4 + 0x2440) = DAT_0060cac4;
      *(undefined2 *)(iVar4 + 0x2442) = DAT_0060cac6;
    }
    else {
      iVar4 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cdb4 + 0x18,0);
      if (iVar4 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_18 = (int)local_10[2];
    switch(local_18) {
    case 0:
      local_10[0x14] = '\0';
      local_10[0x15] = '\0';
      local_10[0x16] = '\0';
      local_10[0x17] = '\0';
      uVar3 = FUN__text__00415040((int)*(short *)(local_c + 2));
      *(undefined4 *)(local_10 + 0x18) = uVar3;
      local_10[2] = local_10[2] + '\x01';
    case 1:
      *(int *)(local_10 + 0x14) = *(int *)(local_10 + 0x14) + *(int *)(local_10 + 0x18);
      if (0xfeff < *(int *)(local_10 + 0x14)) {
        local_10[0x14] = '\0';
        local_10[0x15] = -1;
        local_10[0x16] = '\0';
        local_10[0x17] = '\0';
        if ((*(short *)(local_c + 0xc) == 0) || (iVar4 = FUN__text__00456b20(), iVar4 != 0)) {
          uVar2 = FUN__text__00415070((int)*(short *)(local_c + 4));
          *(undefined2 *)(local_10 + 6) = uVar2;
          local_10[2] = '\x03';
        }
        else {
          local_10[2] = local_10[2] + '\x01';
        }
      }
      break;
    case 2:
      if (((*(uint *)(DAT_007a49fc + 0x1990) & 1) != 0) ||
         ((*(uint *)(DAT_007a49fc + 0x1950) & 0x8000) != 0)) {
        FUN__text__0049ad50(0);
        local_10[2] = '\x04';
        uVar3 = FUN__text__00415040((int)*(short *)(local_c + 6));
        *(undefined4 *)(local_10 + 0x18) = uVar3;
      }
      break;
    case 3:
      *(short *)(local_10 + 6) = *(short *)(local_10 + 6) + -1;
      if (*(short *)(local_10 + 6) == 0) {
        local_10[2] = '\x04';
        uVar3 = FUN__text__00415040((int)*(short *)(local_c + 6));
        *(undefined4 *)(local_10 + 0x18) = uVar3;
      }
      break;
    case 4:
      *(int *)(local_10 + 0x14) = *(int *)(local_10 + 0x14) - *(int *)(local_10 + 0x18);
      if (*(int *)(local_10 + 0x14) < 0x100) {
        local_10[0x14] = '\0';
        local_10[0x15] = '\0';
        local_10[0x16] = '\0';
        local_10[0x17] = '\0';
        local_10[2] = local_10[2] + '\x01';
      }
      break;
    case 5:
      *local_10 = '\0';
      FUN__text__004977a0();
    }
  }
  local_8 = 0x45662b;
  FUN__text__0056ce80();
  return;
}

