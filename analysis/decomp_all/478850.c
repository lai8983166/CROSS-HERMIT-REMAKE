
void FUN__text__00478850(int param_1)

{
  code *pcVar1;
  short sVar2;
  uint uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_6c [16];
  int local_2c;
  undefined2 local_28;
  short local_24;
  int local_20;
  char *local_1c;
  undefined4 local_18;
  int local_14;
  undefined *local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_6c;
  for (iVar4 = 0x1a; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_14 = param_1 + 0x290;
  local_1c = (char *)(param_1 + 0x293);
  local_18 = FUN__text__0047a8e0(param_1);
  local_c = 0;
  if (((*(short *)(param_1 + 0x4f8) != -1) &&
      (iVar4 = FUN__text__00468d10(local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520),
      iVar4 != 0)) &&
     (iVar4 = FUN__text__00469480(local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520),
     iVar4 != 0)) {
    FUN__text__004690a0(local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520);
  }
  local_c = local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520;
  if ((*(short *)(param_1 + 0x4f8) == -1) &&
     (iVar4 = FUN__text__00424f80("wk->dmg_uw!=-1",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e14 + 0x13,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_20 = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40
                            );
  local_10 = &DAT_00611538 + (*(ushort *)(*(int *)(param_1 + 600) + 0xc) + 100) * 0x10;
  local_2c = (int)*local_1c;
  switch(local_2c) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    FUN__text__0046b0b0(param_1,1);
    if (local_c != 0) {
      local_24 = (short)((uint)*(undefined4 *)(local_c + 0x2ec) >> 0x10);
      local_28 = (undefined2)((uint)*(undefined4 *)(local_c + 0x2f0) >> 0x10);
      FUN__text__0046c120(param_1,local_24,CONCAT22(local_24 >> 0xf,local_28));
    }
    uVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e14 + 0x26);
    uVar3 = uVar3 & 0x80000001;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffffe) + 1;
    }
    if (uVar3 == 0) {
      FUN__text__0046bcc0(param_1,9);
    }
    else {
      FUN__text__0046bcc0(param_1,8);
    }
    *(undefined2 *)(param_1 + 0xe) = 0;
    *(undefined2 *)(param_1 + 10) = 0;
    *(undefined2 *)(param_1 + 0x12) = 0x3c;
    *(undefined2 *)(param_1 + 0xc) = 0;
    *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
    *local_1c = *local_1c + '\x01';
    break;
  case 1:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (0x2d < *(short *)(param_1 + 10)) {
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046bcc0(param_1,(int)(char)local_10[2]);
      *local_1c = *local_1c + '\x01';
    }
    break;
  case 2:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (*(short *)(param_1 + 0x10) < 1) {
      FUN__text__0046bcc0(param_1,2);
      *(undefined2 *)(param_1 + 0x10) = 0;
      *local_1c = *local_1c + '\x01';
    }
    break;
  case 3:
    FUN__text__00475460(param_1);
    *(undefined1 *)(param_1 + 0x2a6) = 0;
    FUN__text__0046b0f0(param_1,0);
  }
  local_8 = 0x478ba1;
  FUN__text__0056ce80();
  return;
}

