
void FUN__text__00475f60(int param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = (int)*local_10;
  switch(local_14) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    *(undefined2 *)(param_1 + 0xe) = *(undefined2 *)(&DAT_00618040 + *(char *)(param_1 + 0x260) * 2)
    ;
    *local_10 = *local_10 + '\x01';
    FUN__text__0046bcc0(param_1,0xc);
    FUN__text__00468d80(param_1);
    *(undefined2 *)(param_1 + 0xc) = *(undefined2 *)(param_1 + 0xe);
    FUN__text__0046beb0(param_1,0x80e,0,0,1,0);
    break;
  case 1:
    sVar1 = FUN__text__00415040(1);
    *(short *)(param_1 + 0xc) = *(short *)(param_1 + 0xc) - sVar1;
    if (*(short *)(param_1 + 0xc) < 1) {
      FUN__text__0046b0b0(param_1,1);
      *(undefined2 *)(param_1 + 0xc) = 0;
      *local_10 = *local_10 + '\x01';
      FUN__text__0046bcc0(param_1,0x11);
      FUN__text__0046beb0(param_1,0xffffffff,0,0,1,0);
      FUN__text__0046beb0(param_1,0x812,0,0,1,0);
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      FUN__text__0049ad90(param_1,0x75);
    }
    break;
  case 2:
    if (*(char *)(param_1 + 4) != '\0') {
      *local_10 = *local_10 + '\x01';
      FUN__text__0046bcc0(param_1,0xf);
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      FUN__text__0046b0b0(param_1,0);
      FUN__text__004810d0(param_1);
    }
    break;
  case 3:
    sVar1 = FUN__text__00415040(1);
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar1;
    if (*(short *)(param_1 + 0x10) < 1) {
      *(undefined2 *)(param_1 + 0x10) = 0;
      *local_10 = *local_10 + '\x01';
      FUN__text__0046b0f0(param_1,0);
    }
    break;
  case 4:
    FUN__text__00475270(param_1,2);
  }
  local_8 = 0x4761a4;
  FUN__text__0056ce80();
  return;
}

