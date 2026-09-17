
void FUN__text__00495630(int param_1)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  *(undefined **)(param_1 + 0xc) = (&PTR_DAT_00619668)[*(byte *)(param_1 + 1)];
  *(undefined1 *)(param_1 + 10) = 0;
  *(undefined2 *)(param_1 + 6) = *(undefined2 *)(*(int *)(param_1 + 0xc) + 6);
  local_c = (uint)*(byte *)(param_1 + 1);
  switch(local_c) {
  case 0:
  case 1:
  case 4:
  case 5:
  case 9:
  case 10:
  case 0xd:
  case 0xe:
    iVar3 = FUN__text__00467e70();
    *(char *)(param_1 + 2) = (char)(iVar3 % 0x18) + -0xc;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = -0x2c - (char)uVar2;
    break;
  case 2:
  case 3:
  case 0xb:
  case 0xc:
    iVar3 = FUN__text__00467e70();
    *(char *)(param_1 + 2) = (char)(iVar3 % 0x18) + -0xc;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = -0x2c - (char)uVar2;
    break;
  case 6:
  case 7:
  case 8:
  case 0xf:
  case 0x10:
  case 0x11:
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f58 + 0x26,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 0x12:
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x8000000f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff0) + 1;
    }
    *(char *)(param_1 + 2) = (char)uVar2 + -8;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = (char)uVar2 + -0x2c;
    break;
  case 0x13:
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x8000000f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff0) + 1;
    }
    *(char *)(param_1 + 2) = (char)uVar2 + -8;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = (char)uVar2 + -0x2c;
    break;
  default:
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x8000000f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff0) + 1;
    }
    *(char *)(param_1 + 2) = (char)uVar2 + -8;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = (char)uVar2 + -4;
    break;
  case 0x28:
  case 0x29:
  case 0x2a:
  case 0x2b:
  case 0x2c:
  case 0x2d:
  case 0x2e:
  case 0x2f:
  case 0x30:
  case 0x31:
  case 0x32:
  case 0x33:
  case 0x34:
  case 0x35:
  case 0x36:
  case 0x37:
  case 0x38:
  case 0x39:
  case 0x3a:
  case 0x3b:
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x8000000f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff0) + 1;
    }
    *(char *)(param_1 + 2) = (char)uVar2 + -8;
    uVar2 = FUN__text__00467e70();
    uVar2 = uVar2 & 0x80000007;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff8) + 1;
    }
    *(char *)(param_1 + 3) = (char)uVar2 + -0x2c;
  }
  local_8 = 0x49584d;
  FUN__text__0056ce80();
  return;
}

