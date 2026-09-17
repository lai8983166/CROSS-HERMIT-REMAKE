
void FUN__text__00479410(int param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  undefined *local_14;
  char *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_1c = 0;
  iVar2 = FUN__text__00468d80(param_1);
  if (iVar2 != 0) {
    for (local_18 = 0; local_18 != 0xfa; local_18 = local_18 + 1) {
      iVar2 = FUN__text__00468d10(local_8 + 0x80aec + local_18 * 0x520);
      if ((((iVar2 != 0) &&
           (iVar2 = FUN__text__0046abc0(local_8 + 0x80aec + local_18 * 0x520,param_1), iVar2 != 0))
          && (iVar2 = FUN__text__00468e10(local_8 + 0x80aec + local_18 * 0x520), iVar2 != 0)) &&
         ((iVar2 = FUN__text__004690a0(local_8 + 0x80aec + local_18 * 0x520), iVar2 == 0 &&
          (*(short *)(local_8 + 0x80aee + local_18 * 0x520) != *(short *)(param_1 + 2))))) {
        local_1c = local_1c + 1;
      }
    }
    if (local_1c == 0) {
      FUN__text__0046beb0(param_1,0xffffffff,0,0,1,0);
      FUN__text__00475270(param_1,2);
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046b0f0(param_1,0);
      *(undefined2 *)(param_1 + 0xc) = 0;
      *(undefined2 *)(param_1 + 0x10) = 0;
      goto switchD__text__004795c0_default;
    }
  }
  local_14 = &DAT_006149d0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 10;
  local_20 = (int)*local_10;
  switch(local_20) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    *(undefined2 *)(param_1 + 0xe) = 0xb4;
    *local_10 = *local_10 + '\x01';
    FUN__text__0046bcc0(param_1,0xc);
    *(undefined2 *)(param_1 + 0xc) = *(undefined2 *)(param_1 + 0xe);
    iVar2 = FUN__text__0046cb10(param_1,0x3e);
    if (iVar2 != 0) {
      *(undefined2 *)(param_1 + 0xc) = 2;
    }
    FUN__text__0046beb0(param_1,0x7fc,0,0,1,0);
    FUN__text__0049ad90(param_1,0x72);
    break;
  case 1:
    sVar1 = FUN__text__00415040(1);
    *(short *)(param_1 + 0xc) = *(short *)(param_1 + 0xc) - sVar1;
    if (*(short *)(param_1 + 0xc) < 1) {
      FUN__text__0046b0b0(param_1,1);
      *(undefined2 *)(param_1 + 0xc) = 0;
      FUN__text__0046bcc0(param_1,(int)(char)local_14[2]);
      FUN__text__0046beb0(param_1,0xffffffff,0,0,1,0);
      FUN__text__0046be50(param_1,(int)*(short *)(local_14 + 8),0,0);
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 2:
    if (*(char *)(param_1 + 4) != '\0') {
      *(undefined2 *)(param_1 + 10) = 0;
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 3:
    sVar1 = *(short *)(param_1 + 10);
    iVar2 = FUN__text__00415070(0x46);
    if (iVar2 < sVar1) {
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046b0f0(param_1,0);
      if (*(int *)(*(int *)(param_1 + 600) + 0x24) < 0xe11) {
        FUN__text__00475270(param_1,0xf);
        *(undefined2 *)(param_1 + 0xc) = 0;
        *(undefined2 *)(param_1 + 0x10) = 0;
      }
      else {
        FUN__text__00475370(param_1,0xb,0xffffffff);
        FUN__text__0046ba10(param_1);
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 2;
        *(int *)(*(int *)(param_1 + 600) + 0x24) = *(int *)(*(int *)(param_1 + 600) + 0x24) + -0xe10
        ;
        if (*(int *)(*(int *)(param_1 + 600) + 0x24) < 1) {
          *(undefined4 *)(*(int *)(param_1 + 600) + 0x24) = 0;
        }
      }
    }
  }
switchD__text__004795c0_default:
  local_8 = 0x479807;
  FUN__text__0056ce80();
  return;
}

