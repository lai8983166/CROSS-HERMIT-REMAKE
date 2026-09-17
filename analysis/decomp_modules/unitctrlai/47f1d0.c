
/* WARNING: Removing unreachable block (ram,0x0047f257) */

void FUN__text__0047f1d0(int param_1)

{
  undefined1 uVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  int local_20;
  undefined1 local_1c;
  undefined3 uStack_1b;
  short local_18;
  short local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_20 = (int)*local_10;
  switch(local_20) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    *(undefined2 *)(param_1 + 0xe) = 0xb4;
    *(undefined2 *)(param_1 + 0xc) = *(undefined2 *)(param_1 + 0xe);
    FUN__text__0046bcc0(param_1,0xc);
    *local_10 = *local_10 + '\x01';
    break;
  case 1:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0xc) = *(short *)(param_1 + 0xc) - sVar2;
    if (*(short *)(param_1 + 0xc) < 1) {
      FUN__text__0046b0b0(param_1,1);
      *(undefined2 *)(param_1 + 0xc) = 0;
      FUN__text__0046bcc0(param_1,0x11);
      FUN__text__0046beb0(param_1,0xffffffff,0,0,1,0);
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 2:
    if (*(char *)(param_1 + 4) != '\0') {
      FUN__text__0046bcc0(param_1,0xf);
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      FUN__text__0046b0b0(param_1,0);
      local_14 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                              (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_18 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                              (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      uVar1 = FUN__text__004ddbb0(param_1);
      _local_1c = CONCAT31(uStack_1b,uVar1);
      FUN__text__004807e0(param_1,(int)local_14,(int)local_18,uVar1,
                          *(undefined1 *)(*(int *)(param_1 + 600) + 0x97));
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 3:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (*(short *)(param_1 + 0x10) < 1) {
      *(undefined2 *)(param_1 + 0x10) = 0;
      *local_10 = *local_10 + '\x01';
      FUN__text__0046b0f0(param_1,0);
    }
    break;
  case 4:
    FUN__text__00475270(param_1,2);
  }
  local_8 = 0x47f42b;
  FUN__text__0056ce80();
  return;
}

