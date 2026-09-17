
void FUN__text__0040af40(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                        short param_5,short param_6,undefined4 param_7,byte param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_1;
  local_c = FUN__text__0040b5e0();
  if (local_c != 0) {
    if ((param_8 & 0x80) == 0) {
      *(undefined1 *)(local_c + 3) = *(undefined1 *)(param_1 + 3);
    }
    else {
      *(byte *)(local_c + 3) = param_8 & 0x80;
    }
    *(byte *)(local_c + 3) = *(byte *)(local_c + 3) | 0x40;
    *(undefined4 *)(local_c + 0x24) = *(undefined4 *)(param_1 + 0x24);
    *(undefined4 *)(local_c + 0x1c) = param_2;
    *(undefined1 *)(local_c + 2) = 1;
    local_10 = *(int *)(local_c + 0x24);
    *(undefined4 *)(local_c + 0x20) = *(undefined4 *)(local_10 + 0x20);
    *(int *)(local_10 + 0x20) = local_c;
    if ((*(byte *)(local_c + 3) & 1) == 0) {
      *(short *)(local_c + 0x12) = *(short *)(param_1 + 0x12) + param_5;
    }
    else {
      *(short *)(local_c + 0x12) = *(short *)(param_1 + 0x12) - param_5;
    }
    if ((*(byte *)(local_c + 3) & 2) == 0) {
      *(short *)(local_c + 0x14) = *(short *)(param_1 + 0x14) + param_6;
    }
    else {
      *(short *)(local_c + 0x14) = *(short *)(param_1 + 0x14) - param_6;
    }
    *(char *)(local_c + 8) = *(char *)(param_1 + 8) + '\x01';
    *(undefined4 *)(local_c + 0x18) = param_7;
    if (*(int *)(param_1 + 0x2c) != 0) {
      *(undefined4 *)(local_c + 0x2c) = *(undefined4 *)(param_1 + 0x2c);
      *(undefined4 *)(local_c + 0x48) = *(undefined4 *)(param_1 + 0x48);
      *(undefined4 *)(local_c + 0x4c) = *(undefined4 *)(param_1 + 0x4c);
      *(undefined4 *)(local_c + 0x50) = *(undefined4 *)(param_1 + 0x50);
    }
    FUN__text__0040a400(local_c,param_3,param_4);
    FUN__text__0040a800(local_c);
  }
  local_8 = 0x40b0e8;
  FUN__text__0056ce80();
  return;
}

