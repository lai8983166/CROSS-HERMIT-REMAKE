
void FUN__text__00477980(int param_1)

{
  code *pcVar1;
  short sVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_a4 [16];
  char local_64;
  byte local_60;
  undefined4 local_5c;
  int local_58;
  int local_54;
  int local_50;
  char local_4c;
  char local_48;
  char local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  char *local_30;
  int local_2c;
  int local_28;
  int local_24;
  undefined *local_20;
  undefined *local_1c;
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  char *local_c;
  int local_8;
  
  puVar5 = local_a4;
  for (iVar4 = 0x28; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_2c = param_1 + 0x290;
  local_30 = (char *)(param_1 + 0x293);
  if ((*(short *)(param_1 + 0x4f2) == -1) &&
     (iVar4 = FUN__text__00424f80("wk->bomno!=-1",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e10 + 0xd,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_1c = &DAT_006c2dc8 + *(short *)(param_1 + 0x4f2) * 0x48;
  local_20 = &DAT_006b2d88 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  local_24 = FUN__text__0047a8e0(param_1);
  if ((0xa9 < *(ushort *)(*(int *)(param_1 + 600) + 2)) &&
     (*(ushort *)(*(int *)(param_1 + 600) + 2) < 200)) goto LAB__text__0047869f;
  if ((*local_30 != '\0') &&
     ((*local_30 < '\x14' && (iVar4 = FUN__text__0047ba20(param_1,local_1c), iVar4 == 0)))) {
    FUN__text__00437d90(param_1,0);
    FUN__text__00475270(param_1,2);
    goto LAB__text__0047879a;
  }
  if (('\t' < *local_30) && (*local_30 < '\x14')) {
    local_40 = FUN__text__0047bed0(param_1,local_1c[0x18]);
    local_28 = local_40;
    if (local_40 == 1) {
      FUN__text__00437d90(param_1,0);
      iVar4 = FUN__text__00469ad0(local_8 + 0x80aec + *(short *)(param_1 + 0x4ee) * 0x520);
      if ((((iVar4 == 0) ||
           (iVar4 = FUN__text__0046abc0(param_1,local_8 + 0x80aec +
                                                *(short *)(param_1 + 0x4ee) * 0x520), iVar4 != 0))
          || (iVar4 = FUN__text__0046ad60(param_1,local_8 + 0x80aec +
                                                  *(short *)(param_1 + 0x4ee) * 0x520), iVar4 != 0))
         || ((iVar4 = FUN__text__004698a0(param_1), iVar4 == 0 ||
             (*(char *)(local_24 + 0x1c) != '\0')))) {
        *local_30 = '\x14';
      }
      else {
        FUN__text__00475270(param_1,0x13);
      }
      goto LAB__text__0047879a;
    }
    if (local_40 == 2) {
      FUN__text__00475270(param_1,0xf);
      FUN__text__00437d90(param_1,0);
    }
  }
  if ((*local_30 != '\0') && (*local_30 < '\x14')) {
    iVar4 = FUN__text__0047cc90(param_1);
    if (iVar4 != 0) {
      local_34 = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
      iVar4 = FUN__text__0047b210(param_1,local_34);
      if (iVar4 == 0) {
        FUN__text__00492e60(param_1 + 0x4fa);
      }
      else {
        iVar4 = FUN__text__0047ce70(param_1,local_34);
        if (iVar4 != 0) {
          FUN__text__00437d90(param_1,0);
          goto LAB__text__0047879a;
        }
      }
    }
    iVar4 = FUN__text__004697f0(param_1);
    if (((iVar4 != 0) || (local_44 = *(char *)(local_24 + 0x14), local_44 == '\x01')) &&
       (iVar4 = FUN__text__0047c210(param_1,local_1c[0x18]), iVar4 == 0)) {
      FUN__text__00437d90(param_1,0);
      if (*(char *)(local_24 + 0x16) != '\0') {
        *(char *)(param_1 + 0x2e8) =
             (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                         (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
        *(char *)(param_1 + 0x2e9) =
             (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                         (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      }
      local_48 = *(char *)(local_24 + 0x15);
      if (local_48 == '\0') {
        FUN__text__00475270(param_1,2);
        FUN__text__00437d90(param_1,0);
      }
      else if (local_48 == '\x01') {
        FUN__text__00475270(param_1,0xf);
        FUN__text__00437d90(param_1,0);
      }
      else if (local_48 == '\x02') {
        FUN__text__00475270(param_1,0x16);
        FUN__text__00437d90(param_1,0);
      }
      goto LAB__text__0047879a;
    }
  }
  if ((((('\t' < *local_30) && (iVar4 = FUN__text__004698a0(param_1), iVar4 != 0)) &&
       ((local_4c = *(char *)(local_24 + 0x1b), local_4c == '\x01' &&
        ((local_38 = FUN__text__0047a920(param_1), local_38 != 0 && (*local_30 < '\x14')))))) &&
      (*(short *)(local_38 + 2) !=
       *(short *)(local_8 + 0x80aee + *(short *)(param_1 + 0x4ee) * 0x520))) &&
     (iVar4 = FUN__text__0047b210(param_1,local_38), iVar4 != 0)) {
    local_50 = (int)*(char *)(local_24 + 0x12);
    switch(local_50) {
    case 0:
      if (((*(char *)(local_24 + 0x1c) != '\0') ||
          (iVar4 = FUN__text__00469ad0(local_38), iVar4 == 0)) &&
         (iVar4 = FUN__text__0047c580(param_1,local_38), iVar4 != 0)) {
        FUN__text__00475270(param_1,6);
        FUN__text__00437d90(param_1,0);
        goto LAB__text__0047879a;
      }
      break;
    case 2:
      *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(local_38 + 2);
      FUN__text__00475270(param_1,0x1d);
      FUN__text__00437d90(param_1,0);
      break;
    case 3:
      iVar4 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e10 + 0xb5,0);
      if (iVar4 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 4:
      FUN__text__00475270(param_1,6);
      FUN__text__00437d90(param_1,0);
      goto LAB__text__0047879a;
    }
  }
  local_54 = (int)*local_30;
  switch(local_54) {
  case 0:
    iVar4 = FUN__text__0046c930(param_1,(int)*(short *)(param_1 + 0x4f2));
    if (iVar4 != 0) {
      local_58 = FUN__text__0047bc90(param_1,local_1c[0x18]);
      if (local_58 == 0) {
        if ((*(char *)(local_2c + 0x17) == '\x01') &&
           (*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x02')) {
          *local_30 = '\x12';
        }
        else {
          *local_30 = '\n';
        }
      }
      else if (local_58 == 1) goto LAB__text__0047869f;
      break;
    }
    iVar4 = FUN__text__0046c930(param_1,(int)*(short *)(local_20 + 0x18));
    if (iVar4 != 0) {
      *(undefined2 *)(param_1 + 0x4f2) = *(undefined2 *)(local_20 + 0x18);
      iVar4 = *(int *)(local_8 + 0x80dd8 + *(short *)(param_1 + 0x4ee) * 0x520);
      *(char *)(param_1 + 0x4f0) = (char)((int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0x1fU)) >> 5);
      iVar4 = *(int *)(local_8 + 0x80ddc + *(short *)(param_1 + 0x4ee) * 0x520);
      *(char *)(param_1 + 0x4f1) = (char)((int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0xfU)) >> 4);
      *local_30 = '\0';
      goto LAB__text__0047879a;
    }
    goto LAB__text__0047869f;
  case 10:
    *(undefined1 *)(param_1 + 0x294) = 0;
    *(undefined2 *)(param_1 + 0x4e0) = 0;
    *local_30 = *local_30 + '\x01';
    break;
  case 0xb:
    *local_30 = *local_30 + '\x01';
    break;
  case 0xc:
    local_5c = FUN__text__00476680(param_1,1);
    switch(local_5c) {
    case 0:
      break;
    case 1:
      *local_30 = '\0';
      break;
    case 2:
      goto LAB__text__0047869f;
    case 3:
    case 4:
      goto LAB__text__0047869f;
    default:
      iVar4 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e10 + 0x118,0);
      if (iVar4 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    break;
  case 0x12:
    if (*(char *)(*(int *)(param_1 + 600) + 0x9f) != '\x02') {
      local_60 = *(byte *)(*(int *)(param_1 + 600) + 0x9f);
      if (local_60 < 2) {
        *local_30 = '\0';
      }
      else {
        if (local_60 == 3) goto LAB__text__0047869f;
        iVar4 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e10 + 0x130,0);
        if (iVar4 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
    }
    break;
  case 0x14:
    FUN__text__0046b0f0(param_1,1);
    local_3c = (int)*(short *)(local_20 + 0x18);
    if (local_3c == *(short *)(param_1 + 0x4f2)) {
      *(undefined2 *)(param_1 + 0xe) = *(undefined2 *)(*(int *)(param_1 + 600) + 0x32);
      *(undefined2 *)(param_1 + 0x12) = *(undefined2 *)(*(int *)(param_1 + 600) + 0x34);
    }
    else {
      *(undefined2 *)(param_1 + 0xe) =
           *(undefined2 *)(&DAT_006c2dd2 + *(short *)(param_1 + 0x4f2) * 0x48);
      *(undefined2 *)(param_1 + 0x12) =
           *(undefined2 *)(&DAT_006c2dd6 + *(short *)(param_1 + 0x4f2) * 0x48);
    }
    FUN__text__0048cae0(param_1,(int)*(short *)(param_1 + 0x4f2));
    local_c = &DAT_00611538 + *(short *)(param_1 + 0x4f2) * 0x10;
    *local_30 = *local_30 + '\x01';
    FUN__text__0046c120(param_1,*(undefined2 *)(param_1 + 0x4d0),*(undefined2 *)(param_1 + 0x4d2));
    if (*(short *)(param_1 + 0xe) == 0) {
LAB__text__00478339:
      FUN__text__0046b0b0(param_1,1);
      *(undefined2 *)(param_1 + 0xc) = 0;
      *local_30 = *local_30 + '\x01';
      local_c = &DAT_00611538 + *(short *)(param_1 + 0x4f2) * 0x10;
      if ((*(short *)(param_1 + 0x4ee) == -1) &&
         (iVar4 = FUN__text__00424f80("wk->target!=-1",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e10 + 0x16a,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      _memset(&local_18,0,0xc);
      local_18 = (uint)CONCAT11(*(undefined1 *)(param_1 + 0x4ee),*(undefined1 *)(param_1 + 2)) <<
                 0x10;
      local_14 = CONCAT22(local_14._2_2_,*(undefined2 *)(local_c + 8));
      *(int *)(param_1 + 0x90) = local_18;
      *(undefined4 *)(param_1 + 0x94) = local_14;
      *(undefined4 *)(param_1 + 0x98) = local_10;
      uVar3 = FUN__text__0048ccb0(param_1,(int)*(short *)(param_1 + 0x4f2),(int)local_c[1]);
      FUN__text__0046bcc0(param_1,uVar3);
      FUN__text__0046beb0(param_1,0xffffffff,0,0,1,0);
      if (*(short *)(local_c + 6) != 0) {
        FUN__text__0046beb0(param_1,(int)*(short *)(local_c + 6),0,0,0,&local_18);
      }
      FUN__text__0046c990(param_1,(int)*(short *)(param_1 + 0x4f2));
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      iVar4 = FUN__text__0046c9f0((int)*(short *)(param_1 + 0x4f2));
      if (iVar4 == 0) {
        *(undefined1 *)(*(int *)(param_1 + 600) + 0x9d) = 0;
      }
    }
    else {
      FUN__text__0046bcc0(param_1,(int)*local_c);
      *(undefined2 *)(param_1 + 0xc) = *(undefined2 *)(param_1 + 0xe);
      if (*(short *)(local_c + 4) != 0) {
        FUN__text__0046beb0(param_1,(int)*(short *)(local_c + 4),0,0,1,0);
      }
    }
    break;
  case 0x15:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0xc) = *(short *)(param_1 + 0xc) - sVar2;
    if (*(short *)(param_1 + 0xc) < 1) goto LAB__text__00478339;
    break;
  case 0x16:
    if (*(char *)(param_1 + 4) != '\0') {
      *local_30 = *local_30 + '\x01';
      *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
      iVar4 = *(short *)(param_1 + 0x4f2) * 0x10;
      local_c = &DAT_00611538 + iVar4;
      FUN__text__0046bcc0(param_1,(int)(char)(&DAT_0061153a)[iVar4]);
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0049ad90(param_1,0x6a);
    }
    break;
  case 0x17:
    sVar2 = FUN__text__00415040(1);
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (*(short *)(param_1 + 0x10) < 1) {
      FUN__text__0046bcc0(param_1,2);
      *(undefined2 *)(param_1 + 0x10) = 0;
      FUN__text__0046b0f0(param_1,0);
      *local_30 = *local_30 + '\x01';
    }
    break;
  case 0x18:
    local_64 = *(char *)(local_24 + 0x1d);
    if (local_64 != '\0') {
      if (local_64 == '\x01') {
        if (*(short *)(param_1 + 0x4ee) != -1) {
          *(undefined2 *)(param_1 + 0x4f2) = 0xffff;
          FUN__text__00475270(param_1,0x1d);
          goto LAB__text__0047879a;
        }
      }
      else {
        iVar4 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e10 + 0x1b5,0);
        if (iVar4 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
    }
    if ((((*(short *)(param_1 + 0x4ee) == -1) ||
         ((iVar4 = FUN__text__0046abc0(param_1,local_8 + 0x80aec +
                                               *(short *)(param_1 + 0x4ee) * 0x520), iVar4 == 0 &&
          (iVar4 = FUN__text__0046ad60(param_1,local_8 + 0x80aec +
                                               *(short *)(param_1 + 0x4ee) * 0x520), iVar4 == 0))))
        || ((iVar4 = FUN__text__00469a30(param_1), iVar4 == 0 &&
            (iVar4 = FUN__text__004698a0(param_1), iVar4 == 0)))) &&
       ((iVar4 = FUN__text__00468d80(param_1), iVar4 != 0 &&
        (*(char *)(*(int *)(param_1 + 600) + 0x9f) != '\x03')))) {
      if (*(char *)(*(int *)(param_1 + 600) + 0xa0) == '\x02') {
        iVar4 = FUN__text__0047c210(param_1,CONCAT31((int3)((uint)*(int *)(param_1 + 600) >> 8),
                                                     local_1c[0x18]));
        if (iVar4 != 0) {
          *local_30 = '\0';
          goto LAB__text__0047879a;
        }
      }
      else {
        iVar4 = FUN__text__0046c9f0((int)*(short *)(param_1 + 0x4f2));
        if ((iVar4 != 0) && (iVar4 = FUN__text__0047c210(param_1,local_1c[0x18]), iVar4 != 0)) {
          *local_30 = '\0';
          goto LAB__text__0047879a;
        }
      }
    }
LAB__text__0047869f:
    *(undefined2 *)(param_1 + 0x4ee) = 0xffff;
    *(undefined2 *)(param_1 + 0x4f2) = 0xffff;
    FUN__text__00475270(param_1,0xf);
    goto LAB__text__0047879a;
  }
LAB__text__0047879a:
  local_8 = 0x4787aa;
  FUN__text__0056ce80();
  return;
}

