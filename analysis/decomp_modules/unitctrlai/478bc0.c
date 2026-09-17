
void FUN__text__00478bc0(int param_1)

{
  code *pcVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  float10 fVar5;
  undefined4 local_9c [16];
  int local_5c;
  char local_58;
  int local_54;
  float local_50;
  float local_4c;
  float local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
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
  
  puVar4 = local_9c;
  for (iVar3 = 0x26; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = param_1 + 0x290;
  local_1c = (char *)(param_1 + 0x293);
  local_18 = FUN__text__0047a8e0();
  local_c = 0;
  if (((*(short *)(param_1 + 0x4f8) != -1) && (iVar3 = FUN__text__00468d10(), iVar3 != 0)) &&
     (iVar3 = FUN__text__00469480(), iVar3 != 0)) {
    FUN__text__004690a0();
  }
  local_c = local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520;
  if ((*(short *)(param_1 + 0x4f8) == -1) &&
     (iVar3 = FUN__text__00424f80("wk->dmg_uw!=-1",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e18 + 0x25,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_20 = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40
                            );
  local_10 = &DAT_00611538 + (*(ushort *)(*(int *)(param_1 + 600) + 0xc) + 100) * 0x10;
  local_54 = (int)*local_1c;
  switch(local_54) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    FUN__text__0046b0b0(param_1,1);
    if (local_c != 0) {
      local_24 = (short)((uint)*(undefined4 *)(local_c + 0x2ec) >> 0x10);
      local_28 = (undefined2)((uint)*(undefined4 *)(local_c + 0x2f0) >> 0x10);
      FUN__text__0046c120(param_1,local_24,CONCAT22(local_24 >> 0xf,local_28));
    }
    FUN__text__0046bcc0(param_1,8);
    *(undefined2 *)(param_1 + 0xe) = 0;
    *(undefined2 *)(param_1 + 10) = 0;
    *(undefined2 *)(param_1 + 0x12) = 0x5a;
    *(undefined2 *)(param_1 + 0xc) = 0;
    *(undefined2 *)(param_1 + 0x10) = *(undefined2 *)(param_1 + 0x12);
    *local_1c = *local_1c + '\x01';
    break;
  case 1:
    if ((*(short *)(param_1 + 10) < 0x20) && (*(char *)(param_1 + 0x4f6) != -1)) {
      local_34 = *(undefined4 *)(param_1 + 0x2ec);
      local_38 = *(undefined4 *)(param_1 + 0x2f0);
      local_58 = *(char *)(param_1 + 0x4f6);
      if (local_58 == '\0') {
        local_2c = (*(int *)(param_1 + 0x2ec) >> 0x10) + (uint)*(byte *)(param_1 + 0x4f4) * -0x20;
        local_30 = (*(int *)(param_1 + 0x2f0) >> 0x10) + (uint)*(byte *)(param_1 + 0x4f5) * -0x10;
      }
      else if (local_58 == '\x01') {
        local_2c = *(int *)(param_1 + 0x2ec) - *(int *)(local_c + 0x2ec) >> 0x10;
        local_30 = *(int *)(param_1 + 0x2f0) - *(int *)(local_c + 0x2f0) >> 0x10;
      }
      else {
        iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e18 + 0x59,0);
        if (iVar3 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_5c = local_2c * local_2c + local_30 * local_30;
      fVar5 = (float10)FUN__text__005711e4((double)local_5c);
      local_50 = (float)fVar5;
      local_48 = (float)local_2c / local_50;
      local_4c = (float)local_30 / local_50;
      DAT_00618cf0 = (int)*(short *)(&DAT_00618cf8 + *(short *)(param_1 + 10) * 2) << 0x10;
      DAT_00618cf4 = (int)*(short *)(&DAT_00618cf8 + *(short *)(param_1 + 10) * 2) / 2 << 0x10;
      local_2c = __ftol();
      local_30 = __ftol();
      iVar3 = local_2c + *(int *)(param_1 + 0x2ec);
      local_34 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5;
      iVar3 = local_30 + *(int *)(param_1 + 0x2f0);
      local_38 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4;
      local_3c = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                      (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_40 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                      (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      if ((0 < local_34) && (0 < local_38)) {
        local_44 = 0;
        iVar3 = FUN__text__0043bfa0(local_34,local_38,
                                    *(undefined1 *)(*(int *)(param_1 + 600) + 0x30));
        if (iVar3 != 0) {
          if ((local_34 == local_3c) && (local_38 == local_40)) {
            iVar3 = FUN__text__0043c0c0(local_34,local_38);
            if (iVar3 == 1) {
              local_44 = 1;
            }
          }
          else {
            iVar3 = FUN__text__0043c0c0(local_34,local_38);
            if (iVar3 == 0) {
              local_44 = 1;
            }
          }
          if (local_44 != 0) {
            *(int *)(param_1 + 0x2ec) = *(int *)(param_1 + 0x2ec) + local_2c;
            *(int *)(param_1 + 0x2f0) = *(int *)(param_1 + 0x2f0) + local_30;
            local_3c = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                            (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
            local_40 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                            (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
            iVar3 = FUN__text__0043bfa0(local_3c,local_40,
                                        *(undefined1 *)(*(int *)(param_1 + 600) + 0x30));
            if ((iVar3 == 0) &&
               (iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                            "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                            DAT_00618e18 + 0x83,0), iVar3 != 0)) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
        }
      }
    }
    sVar2 = FUN__text__00415040();
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (0x3c < *(short *)(param_1 + 10)) {
      FUN__text__0046b0b0(param_1,0);
      FUN__text__0046bcc0(param_1,(int)(char)local_10[2]);
      *local_1c = *local_1c + '\x01';
    }
    break;
  case 2:
    sVar2 = FUN__text__00415040();
    *(short *)(param_1 + 0x10) = *(short *)(param_1 + 0x10) - sVar2;
    if (*(short *)(param_1 + 0x10) < 1) {
      FUN__text__0046bcc0(param_1,2);
      *(undefined2 *)(param_1 + 0x10) = 0;
      *local_1c = *local_1c + '\x01';
    }
    break;
  case 3:
    FUN__text__00475460();
    *(undefined1 *)(param_1 + 0x2a6) = 0;
    FUN__text__0046b0f0(param_1,0);
  }
  local_8 = 0x47924c;
  FUN__text__0056ce80();
  return;
}

