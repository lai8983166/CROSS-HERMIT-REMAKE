
void FUN__text__004799c0(int param_1)

{
  code *pcVar1;
  int iVar2;
  short sVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  short local_20;
  int local_1c;
  char local_18;
  char *local_14;
  char *local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = &DAT_006149d0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 10;
  local_28 = (int)*local_10;
  switch(local_28) {
  case 0:
    FUN__text__0046b0b0(param_1,1);
    FUN__text__0046b0f0(param_1,1);
    local_18 = *(char *)(*(int *)(param_1 + 600) + 0xae) + '\x01';
    if (*(char *)(*(int *)(param_1 + 600) + 0xae) < local_18) {
      *(char *)(*(int *)(param_1 + 600) + 0xae) = local_18;
    }
    if ((-1 < *(short *)(*(int *)(param_1 + 600) + 0xa6)) &&
       (*(short *)(*(int *)(param_1 + 600) + 0xa6) < 0xfa)) {
      local_1c = local_8 + 0x80aec + *(short *)(*(int *)(param_1 + 600) + 0xa6) * 0x520;
      iVar2 = FUN__text__00468d10(local_1c);
      if ((iVar2 == 0) &&
         (iVar2 = FUN__text__00424f80("IsUwUsed(wkt)",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e1c + 0x17,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      sVar3 = *(short *)(*(int *)(local_1c + 600) + 0xaa) + 1;
      if (*(short *)(*(int *)(local_1c + 600) + 0xaa) < sVar3) {
        *(short *)(*(int *)(local_1c + 600) + 0xaa) = sVar3;
      }
      sVar3 = *(short *)(*(int *)(local_1c + 600) + 0xac) +
              *(short *)(*(int *)(param_1 + 600) + 0xa8);
      if (*(short *)(*(int *)(local_1c + 600) + 0xac) < sVar3) {
        *(short *)(*(int *)(local_1c + 600) + 0xac) = sVar3;
      }
      local_20 = *(short *)(local_8 + 0x2ef14 + (uint)*(byte *)(*(int *)(local_1c + 600) + 0xa4) * 2
                           ) + *(short *)(*(int *)(param_1 + 600) + 0xa8);
      if (*(short *)(local_8 + 0x2ef14 + (uint)*(byte *)(*(int *)(local_1c + 600) + 0xa4) * 2) <
          local_20) {
        *(short *)(local_8 + 0x2ef14 + (uint)*(byte *)(*(int *)(local_1c + 600) + 0xa4) * 2) =
             local_20;
      }
    }
    FUN__text__00430b20(param_1);
    *local_10 = *local_10 + '\x01';
    FUN__text__0046bcc0(param_1,(int)*local_14);
    FUN__text__0046be50(param_1,(int)*(short *)(local_14 + 4),0,0);
    FUN__text__0049ad90(param_1,0x71);
    break;
  case 1:
    if (*(char *)(param_1 + 4) != '\0') {
      *local_10 = *local_10 + '\x01';
      *(undefined2 *)(param_1 + 10) = 0;
    }
    break;
  case 2:
    sVar3 = *(short *)(param_1 + 10);
    iVar2 = FUN__text__00415070(0x46);
    if (iVar2 < sVar3) {
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046b0f0(param_1,0);
      iVar2 = FUN__text__00468d80(param_1);
      if (iVar2 == 0) {
        FUN__text__0046ba10(param_1);
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 3;
      }
      else {
        FUN__text__0046ba10(param_1);
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 3;
        iVar2 = FUN__text__00468eb0(param_1);
        if ((iVar2 == 0) || (0xe0f < *(int *)(*(int *)(param_1 + 600) + 0x24))) {
          iVar2 = FUN__text__0046cb10(param_1,0x54);
          if (iVar2 == 0) {
            local_24 = 0x32;
          }
          else {
            local_24 = 0x4b;
          }
          *(int *)(*(int *)(param_1 + 600) + 0x24) =
               (*(int *)(*(int *)(param_1 + 600) + 0x24) * local_24) / 100;
          if (*(int *)(*(int *)(param_1 + 600) + 0x24) < 1) {
            *(undefined4 *)(*(int *)(param_1 + 600) + 0x24) = 0;
          }
        }
        else {
          *(undefined4 *)(*(int *)(param_1 + 600) + 0x24) = 0;
          *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 4;
        }
      }
      *local_10 = *local_10 + '\x01';
      FUN__text__00475370(param_1,0xb,0xffffffff);
    }
    break;
  case 3:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e1c + 0x57,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x479e1f;
  FUN__text__0056ce80();
  return;
}

