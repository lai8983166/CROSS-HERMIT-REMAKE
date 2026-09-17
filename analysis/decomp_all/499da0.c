
void __fastcall FUN__text__00499da0(int param_1)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  char *local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x108b3e);
  local_10 = *(int *)(DAT_007a49fc + 0x196c);
  local_14 = *(int *)(DAT_007a49fc + 0x1970);
  local_20 = (int)*(char *)(param_1 + 0x108b4a);
  local_8 = param_1;
  switch(local_20) {
  case 0:
    local_18 = *(short *)(param_1 + 0x108b40) * 0x20 + 0x10;
    local_1c = *(short *)(param_1 + 0x108b42) * 0x10 + 8;
    FUN__text__0043b400((int)local_18,(int)local_1c);
    if (*(char *)(*(int *)(local_8 + 0x117c38) + 0x170) != '\0') {
      if (*local_c == '\0') {
        local_c[0xc] = '\x04';
      }
      else if (*(short *)(local_c + 0xe) == 0) {
        if (local_c[0xd] == local_c[6]) {
          local_c[0xc] = local_c[0xc] + '\x01';
        }
        else {
          local_c[0xd] = local_c[0xd] + '\x01';
          uVar1 = FUN__text__00415070(5);
          *(undefined2 *)(local_c + 0xe) = uVar1;
        }
      }
      else {
        *(short *)(local_c + 0xe) = *(short *)(local_c + 0xe) + -1;
      }
    }
    break;
  case 1:
    FUN__text__0043b250(2);
    *(undefined1 *)(local_8 + 0x108b36) = 1;
    *(undefined1 *)(local_8 + 0x108b37) = 1;
    if ((*(int *)(local_8 + 0x108b50) < (int)local_c[8]) ||
       ((int)local_c[7] < *(int *)(local_8 + 0x108b50))) {
      local_c[9] = '\x02';
    }
    else {
      local_c[9] = '\0';
      if ((((*(int *)(DAT_007a49fc + 0x19b8) != 0) && (0x1df < local_10)) && (local_10 < 0x308)) &&
         (((0x2dd < local_14 && (local_14 < 0x2f8)) &&
          (local_c[9] = '\x01', *(int *)(DAT_007a49fc + 0x19b8) == 3)))) {
        FUN__text__0049ad50(5);
        *(undefined1 *)(local_8 + 0x108b36) = 0;
        *(undefined1 *)(local_8 + 0x108b37) = 0;
        uVar1 = FUN__text__00415070(4);
        *(undefined2 *)(local_c + 0xe) = uVar1;
        FUN__text__0043b250(1);
        local_c[0xc] = local_c[0xc] + '\x01';
      }
    }
    break;
  case 2:
    if (*(short *)(param_1 + 0x108b4c) == 0) {
      *(undefined1 *)(param_1 + 0x108b47) = 0;
      *(char *)(param_1 + 0x108b4a) = *(char *)(param_1 + 0x108b4a) + '\x01';
    }
    else {
      *(short *)(param_1 + 0x108b4c) = *(short *)(param_1 + 0x108b4c) + -1;
    }
    break;
  case 3:
    FUN__text__0049a310();
    local_c[0xc] = local_c[0xc] + '\x01';
    break;
  case 4:
    *(undefined1 *)(*(int *)(param_1 + 0x117c38) + 0x170) = 0;
    *(undefined1 *)(param_1 + 0x108b34) = 1;
    *(char *)(param_1 + 0x108b4a) = *(char *)(param_1 + 0x108b4a) + '\x01';
    uVar1 = FUN__text__00415070(0xb4);
    *(undefined2 *)(local_c + 0xe) = uVar1;
    break;
  case 5:
    if (*(short *)(param_1 + 0x108b4c) == 0) {
      *(undefined1 *)(param_1 + 0x108b34) = 0;
      *(char *)(param_1 + 0x108b4a) = *(char *)(param_1 + 0x108b4a) + '\x01';
    }
    else {
      *(short *)(param_1 + 0x108b4c) = *(short *)(param_1 + 0x108b4c) + -1;
    }
    break;
  case 6:
    iVar2 = FUN__text__00456b20();
    if ((iVar2 == 0) || (iVar2 = FUN__text__004daae0((int)DAT_007f4488), iVar2 != 0)) {
      iVar2 = FUN__text__004551c0(0,1);
      if (iVar2 == 0) {
        FUN__text__004549d0(0,0,0,0,1,0,0);
      }
      else {
        FUN__text__004549d0(0,0,1,0,1,1,0);
      }
    }
    else {
      FUN__text__004549d0(0,0,0,0,1,0,0);
    }
    local_c[0xc] = local_c[0xc] + '\x01';
    break;
  case 7:
    iVar2 = FUN__text__00454c40();
    if (iVar2 == 2) {
      local_c[0xc] = local_c[0xc] + '\x01';
    }
    break;
  case 8:
    *(char *)(param_1 + 0x108b4a) = *(char *)(param_1 + 0x108b4a) + '\x01';
    if (DAT_007f44b9 != '\0') {
      FUN__text__004998b0(0);
      break;
    }
    goto LAB__text__0049a1bc;
  case 9:
    iVar2 = FUN__text__00499910();
    if (iVar2 == 0) break;
LAB__text__0049a1bc:
    FUN__text__00454c80();
    local_c[0xc] = local_c[0xc] + '\x01';
    break;
  case 10:
    iVar2 = FUN__text__00454c40();
    if (iVar2 == 0) {
      local_c[0xc] = local_c[0xc] + '\x01';
    }
    break;
  case 0xb:
    *(char *)(param_1 + 0x108b4a) = *(char *)(param_1 + 0x108b4a) + '\x01';
    if (DAT_007f44ba != '\0') {
      FUN__text__004998b0(1);
      break;
    }
    goto LAB__text__0049a23f;
  case 0xc:
    iVar2 = FUN__text__00499910();
    if (iVar2 == 0) break;
LAB__text__0049a23f:
    local_c[0xc] = local_c[0xc] + '\x01';
    break;
  case 0xd:
    *(undefined1 *)(param_1 + 0x108b34) = 1;
    *(undefined1 *)(param_1 + 0x108b35) = 1;
    *(undefined1 *)(param_1 + 0x108b36) = 1;
    *(undefined1 *)(param_1 + 0x108b38) = 1;
    *(undefined1 *)(param_1 + 0x108b39) = 1;
    *(undefined1 *)(param_1 + 0x108b3a) = 1;
    FUN__text__00455160(1);
    local_c[10] = '\0';
    FUN__text__0043b250(0);
  }
  local_8 = 0x49a2cb;
  FUN__text__0056ce80();
  return;
}

