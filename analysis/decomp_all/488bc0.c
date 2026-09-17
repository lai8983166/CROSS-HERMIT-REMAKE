
void FUN__text__00488bc0(int param_1,int param_2,undefined4 *param_3)

{
  code *pcVar1;
  short sVar2;
  short sVar3;
  undefined2 uVar4;
  int iVar5;
  int iVar6;
  undefined4 *puVar7;
  undefined4 uVar8;
  undefined4 local_144 [16];
  int local_104;
  int local_100;
  uint local_fc;
  uint local_f8;
  uint local_f4;
  byte local_f0;
  uint local_ec;
  char local_e8;
  int local_e4;
  int local_e0;
  char local_dc;
  int local_d8;
  int local_d4;
  int local_d0;
  int local_cc;
  int local_c8;
  int local_c4;
  short local_c0;
  uint local_bc;
  uint local_b8;
  uint local_b4;
  uint local_b0;
  int local_ac;
  int local_a8;
  undefined4 local_a4;
  uint local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int *local_90;
  int *local_8c;
  undefined *local_88;
  int local_84;
  undefined *local_80;
  undefined *local_7c;
  undefined *local_78;
  int local_74;
  undefined1 local_70 [44];
  undefined1 local_44 [40];
  short local_1c;
  undefined4 local_18;
  undefined2 local_14;
  char cStack_12;
  undefined1 uStack_11;
  undefined2 local_10;
  short sStack_e;
  int *local_c;
  int local_8;
  
  puVar7 = local_144;
  for (iVar5 = 0x50; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  iVar5 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  local_80 = &DAT_006b2d88 + iVar5;
  local_78 = &DAT_006c2dc8 + *(short *)(param_3 + 1) * 0x48;
  local_7c = &DAT_006c2dc8 + *(short *)(&DAT_006b2da0 + iVar5) * 0x48;
  local_84 = FUN__text__004de8f0((int)*(short *)(param_3 + 1));
  iVar5 = *(short *)(param_3 + 1) * 0x10;
  local_88 = &DAT_00611538 + iVar5;
  local_8c = (int *)(local_8 + 0xddc88);
  local_90 = (int *)(local_8 + 0xde074);
  local_dc = *(char *)((int)param_3 + 7);
  if (local_dc == '\0') {
    if (*(short *)(&DAT_00611542 + iVar5) != 0) {
      *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
      local_e0 = (byte)local_78[0x18] - 1;
      switch(local_e0) {
      case 0:
      case 1:
      case 2:
      case 5:
        *(char *)(param_3 + 2) =
             (char)((int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                         (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
        *(char *)((int)param_3 + 9) =
             (char)((int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                         (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
        local_c4 = 0;
        local_c8 = 0;
        FUN__text__0046beb0(param_2,(int)*(short *)(&DAT_00611542 + iVar5),0,0,0,param_3);
        break;
      case 3:
      case 4:
        *(undefined1 *)(param_3 + 2) = *(undefined1 *)(param_1 + 0x4f0);
        *(undefined1 *)((int)param_3 + 9) = *(undefined1 *)(param_1 + 0x4f1);
        local_cc = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                        (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_d0 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                        (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        local_c4 = ((uint)*(byte *)(param_1 + 0x4f0) - local_cc) * 0x20 + 0x10;
        local_c8 = ((uint)*(byte *)(param_1 + 0x4f1) - local_d0) * 0x10 + 8;
        FUN__text__0046beb0(param_1,(int)*(short *)(&DAT_00611542 + iVar5),local_c4,local_c8,0,
                            param_3);
        break;
      default:
        iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0x27,0);
        if (iVar5 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      goto LAB__text__00489980;
    }
    *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
  }
  else if (local_dc != '\x01') {
    if ((local_dc == '\x02') &&
       (iVar5 = FUN__text__00424f80(&DAT_0059e25c,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0x164,0), iVar5 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__00489980;
  }
  *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
  FUN__text__00488af0((int)*(short *)(param_3 + 1),param_1,local_44);
  local_a0 = FUN__text__004ddc60(param_1,(int)*(short *)(param_3 + 1));
  local_a0 = local_a0 & 0xff;
  local_a4 = FUN__text__004ddd50(param_1,(int)*(short *)(param_3 + 1));
  if (*(short *)(local_88 + 10) == 0) {
    local_e4 = (byte)local_78[0x18] - 1;
    switch(local_e4) {
    case 0:
    case 1:
    case 2:
    case 5:
      local_b0 = (int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                      (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_b4 = (int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                      (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      break;
    case 3:
    case 4:
      local_b0 = (uint)*(byte *)(param_1 + 0x4f0);
      local_b4 = (uint)*(byte *)(param_1 + 0x4f1);
      break;
    default:
      iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f64 + 0x5c,0);
      if (iVar5 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__00489980;
    }
  }
  else {
    local_b0 = (uint)*(byte *)(param_3 + 2);
    local_b4 = (uint)*(byte *)((int)param_3 + 9);
  }
  *local_8c = 0;
  local_e8 = local_88[0xe];
  if (-1 < local_e8) {
    if (local_e8 < '\x05') {
      local_c = (int *)(local_8 + 0xdc8ec);
      local_9c = 0;
      for (local_98 = 0; local_98 != *local_c; local_98 = local_98 + 1) {
        local_d4 = local_c[local_98 + 1];
        iVar5 = FUN__text__0048c950((int)*(short *)(param_3 + 1),param_1,local_d4);
        if (iVar5 != 0) {
          local_a8 = (int)((*(int *)(local_d4 + 0x2ec) >> 0x10) +
                          (*(int *)(local_d4 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
          local_ac = (int)((*(int *)(local_d4 + 0x2f0) >> 0x10) +
                          (*(int *)(local_d4 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
          iVar5 = FUN__text__0043c1d0(local_b0,local_b4,local_a8,local_ac,local_a4);
          if (iVar5 != 0) {
            local_8c[*local_8c + 1] = local_d4;
            *local_8c = *local_8c + 1;
          }
        }
      }
    }
    else if (local_e8 == '\x05') {
      *local_90 = 0;
      local_c = (int *)(local_8 + 0xdc8ec);
      for (local_9c = 0; local_9c != *local_c; local_9c = local_9c + 1) {
        local_d8 = local_c[local_9c + 1];
        iVar5 = FUN__text__0048c950((int)*(short *)(param_3 + 1),param_1,local_d8);
        if (iVar5 != 0) {
          local_90[*local_90 + 1] = local_d8;
          *local_90 = *local_90 + 1;
        }
      }
      if (*local_90 == 0) goto LAB__text__00489980;
      FUN__text__00489df0(local_8 + 0xde460,local_90);
      local_b8 = local_b0;
      local_bc = local_b4;
      local_98 = 0;
      while ((local_98 != *local_90 &&
             (iVar5 = FUN__text__00489e70(local_b8,local_bc,local_8 + 0xde460,local_8c,local_a4),
             iVar5 != 0))) {
        local_b8 = (int)((*(int *)(local_8c[*local_8c] + 0x2ec) >> 0x10) +
                        (*(int *)(local_8c[*local_8c] + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_bc = (int)((*(int *)(local_8c[*local_8c] + 0x2f0) >> 0x10) +
                        (*(int *)(local_8c[*local_8c] + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        local_98 = local_98 + 1;
      }
      if (*local_8c == 0) goto LAB__text__00489980;
    }
  }
  FUN__text__00489a60(local_b0,local_b4,local_8c,local_84,local_78,local_88);
  local_98 = 0;
  while (local_98 != *local_8c) {
    local_94 = local_8c[local_98 + 1];
    local_a8 = (int)((*(int *)(local_94 + 0x2ec) >> 0x10) +
                    (*(int *)(local_94 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
    local_ac = (int)((*(int *)(local_94 + 0x2f0) >> 0x10) +
                    (*(int *)(local_94 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
    FUN__text__004deaa0(local_94,local_70);
    FUN__text__0046b3e0(local_94,local_70);
    if (*(short *)(local_88 + 0xc) == 0) {
      local_f8 = (uint)(byte)local_7c[5];
      switch(local_f8) {
      case 0:
      case 3:
        iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0xef,0);
        if (iVar5 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        break;
      case 1:
      case 4:
        local_74 = FUN__text__004824d0(local_44,local_70);
        break;
      case 2:
        local_74 = FUN__text__004826f0(local_44,local_70);
      }
    }
    else {
      local_ec = (uint)(byte)local_78[5];
      switch(local_ec) {
      case 0:
      case 3:
        iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0xbd,0);
        if (iVar5 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        break;
      case 1:
      case 4:
        local_f0 = *(byte *)(local_84 + 6);
        if (local_f0 == 0) {
          local_74 = 1;
        }
        else if ((local_f0 == 0) || (3 < local_f0)) {
          iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f64 + 0xcf,0);
          if (iVar5 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else {
          local_74 = FUN__text__004824d0(local_44,local_70);
        }
        break;
      case 2:
        local_f4 = (uint)*(byte *)(local_84 + 6);
        switch(local_f4) {
        case 0:
          local_74 = 1;
          break;
        case 1:
        case 2:
        case 3:
          local_74 = FUN__text__004826f0(local_44,local_70);
          break;
        case 4:
        case 5:
        case 6:
          local_74 = FUN__text__00482810(local_44,local_70);
          break;
        default:
          iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f64 + 0xe4,0);
          if (iVar5 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
    }
    if ((local_74 != 0) && (iVar5 = FUN__text__004692e0(local_94), iVar5 != 0)) {
      local_74 = 1;
    }
    local_14 = (undefined2)param_3[1];
    local_10 = (undefined2)param_3[2];
    sStack_e = (short)((uint)param_3[2] >> 0x10);
    cStack_12 = (char)local_74;
    uStack_11 = 2;
    local_18 = CONCAT13(*(undefined1 *)(local_94 + 2),(int3)*param_3);
    local_fc = (uint)*(byte *)(local_84 + 6);
    switch(local_fc) {
    case 0:
      sStack_e = 0;
      break;
    case 1:
    case 2:
    case 3:
      sStack_e = -local_1c;
      break;
    case 4:
    case 5:
    case 6:
      sStack_e = local_1c;
      break;
    default:
      iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f64 + 0x111,0);
      if (iVar5 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_100 = (char)local_88[0xe] + -1;
    switch(local_100) {
    case 0:
      local_18._0_2_ = (short)local_98 * DAT_00618ee8 + 10;
      break;
    case 1:
      local_18._0_2_ = ((short)*local_8c - (short)local_98) * DAT_00618eea + 10;
      break;
    case 2:
      sVar2 = FUN__text__0056db00(local_b0 - local_a8);
      sVar3 = FUN__text__0056db00(local_b4 - local_ac);
      local_c0 = (sVar2 + sVar3) * DAT_00618eec;
      local_18._0_2_ = local_c0 + 10;
      break;
    case 3:
      sVar2 = FUN__text__0056db00(local_b0 - local_a8);
      sVar3 = FUN__text__0056db00(local_b4 - local_ac);
      local_c0 = (sVar2 + sVar3) * DAT_00618eee;
      local_18._0_2_ = 0x8a - local_c0;
      if ((short)local_18 < 10) {
        local_18._0_2_ = 10;
      }
      break;
    case 4:
      local_18._0_2_ = (short)local_98 * DAT_00618ef2 + 10;
      break;
    default:
      sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f64 + 0x119);
      local_18._0_2_ = sVar2 % 0x32 + 10;
    }
    uVar4 = FUN__text__00415070((int)(short)local_18);
    local_18 = CONCAT22(local_18._2_2_,uVar4);
    local_104 = (byte)local_78[0x18] - 1;
    switch(local_104) {
    case 0:
    case 1:
    case 2:
    case 5:
      if ((ushort)*(byte *)((int)param_3 + 3) == *(ushort *)(local_94 + 2)) {
        local_18 = (uint)local_18._2_2_ << 0x10;
      }
    case 3:
    case 4:
      if (*(short *)(local_88 + 0xc) == 0) {
        FUN__text__00482d60((int)*(short *)(local_80 + 0x18),local_74,param_1,local_94,&local_18);
        if (cStack_12 != '\0') {
          FUN__text__0048b2e0(*(undefined1 *)(*(int *)(param_1 + 600) + 0x45),
                              (int)*(short *)(param_3 + 1),param_1,local_94,local_44,local_70);
        }
      }
      else {
        puVar7 = &local_18;
        uVar8 = 0;
        iVar5 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0x148);
        iVar6 = iVar5 % 0x14 + -10;
        iVar5 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f64 + 0x148);
        FUN__text__0046beb0(local_94,(int)*(short *)(local_88 + 0xc),iVar5 % 0x14 + -10,iVar6,uVar8,
                            puVar7);
      }
      local_9c = local_9c + 1;
      local_98 = local_98 + 1;
      break;
    default:
      iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f64 + 0x134,0);
      if (iVar5 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__00489980;
    }
  }
LAB__text__00489980:
  local_8 = 0x489990;
  FUN__text__0056ce80();
  return;
}

