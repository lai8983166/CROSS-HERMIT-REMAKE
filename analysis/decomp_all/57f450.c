
int FUN__text__0057f450(int param_1,byte *param_2,undefined4 *param_3)

{
  byte bVar1;
  code *pcVar2;
  byte bVar3;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  byte *pbVar7;
  bool bVar8;
  longlong lVar9;
  uint local_228;
  uint local_224;
  uint local_220;
  uint local_21c;
  uint local_218;
  uint local_214;
  uint local_210;
  uint local_20c;
  uint local_200;
  uint local_1fc;
  byte local_1f4;
  undefined1 local_1f3;
  uint local_1f0;
  int local_1ec;
  uint *local_1e8;
  byte *local_1e4;
  int local_1e0;
  uint local_1dc;
  undefined4 *local_1d8;
  byte local_1d4;
  byte local_1d3 [351];
  char local_74;
  int local_70;
  char local_6c;
  char local_68;
  byte local_64 [11];
  undefined1 local_59;
  uint local_44;
  uint *local_40;
  char local_3c;
  uint local_38;
  undefined8 local_34;
  char local_2c;
  uint local_28;
  uint local_24;
  int local_20;
  char local_1c;
  char local_18;
  byte local_14;
  uint local_10;
  uint local_c;
  undefined2 local_8 [2];
  
  if ((param_2 == (byte *)0x0) &&
     (iVar4 = FUN__text__00573780(2,"input.c",0x109,0,"format != NULL"), iVar4 == 1)) {
    pcVar2 = (code *)swi(3);
    iVar4 = (*pcVar2)();
    return iVar4;
  }
  if ((param_1 == 0) &&
     (iVar4 = FUN__text__00573780(2,"input.c",0x10c,0,"stream != NULL"), iVar4 == 1)) {
    pcVar2 = (code *)swi(3);
    iVar4 = (*pcVar2)();
    return iVar4;
  }
  local_2c = '\0';
  local_38 = 0;
  local_24 = local_38;
  do {
    if (*param_2 == 0) {
LAB__text__0058073a:
      if ((local_1dc == 0xffffffff) && ((local_38 == 0 && (local_2c == '\0')))) {
        local_228 = 0xffffffff;
        local_38 = local_228;
      }
      return local_38;
    }
    if (DAT_00764370 < 2) {
      local_1fc = *(ushort *)(PTR_DAT_00764164 + (uint)*param_2 * 2) & 8;
    }
    else {
      local_1fc = FUN__text__0057bb50(*param_2,8);
    }
    if (local_1fc != 0) {
      local_24 = local_24 - 1;
      uVar5 = __whiteout(&local_24,param_1,param_1);
      FUN__text__005808f0(uVar5);
      do {
        param_2 = param_2 + 1;
        iVar4 = FUN__text__00571910(*param_2);
      } while (iVar4 != 0);
    }
    if (*param_2 == 0x25) {
      local_44 = 0;
      local_c = local_c & 0xffffff00;
      local_70 = 0;
      local_1ec = 0;
      local_20 = 0;
      local_14 = 0;
      local_6c = '\0';
      local_74 = '\0';
      local_1c = '\0';
      local_68 = '\0';
      local_18 = '\0';
      local_3c = '\x01';
      local_1e0 = 0;
LAB__text__0057f5c5:
      if (local_1c == '\0') {
        pbVar7 = param_2 + 1;
        local_10 = (uint)*pbVar7;
        if (DAT_00764370 < 2) {
          local_200 = *(ushort *)(PTR_DAT_00764164 + local_10 * 2) & 4;
        }
        else {
          local_200 = FUN__text__0057bb50(local_10,4);
        }
        if (local_200 == 0) {
          switch(local_10) {
          case 0x2a:
            local_74 = local_74 + '\x01';
            param_2 = pbVar7;
            break;
          case 0x46:
          case 0x4e:
            param_2 = pbVar7;
            break;
          case 0x49:
            if ((param_2[2] == 0x36) && (param_2[3] == 0x34)) {
              local_1e0 = local_1e0 + 1;
              local_34 = 0;
              param_2 = param_2 + 3;
              break;
            }
          default:
            local_1c = local_1c + '\x01';
            param_2 = pbVar7;
            break;
          case 0x4c:
            local_3c = local_3c + '\x01';
            param_2 = pbVar7;
            break;
          case 0x68:
            local_3c = local_3c + -1;
            local_18 = local_18 + -1;
            param_2 = pbVar7;
            break;
          case 0x6c:
            local_3c = local_3c + '\x01';
          case 0x77:
            local_18 = local_18 + '\x01';
            param_2 = pbVar7;
          }
        }
        else {
          local_1ec = local_1ec + 1;
          local_20 = (local_10 - 0x30) + local_20 * 10;
          param_2 = pbVar7;
        }
        goto LAB__text__0057f5c5;
      }
      if (local_74 == '\0') {
        local_1d8 = param_3;
        local_40 = (uint *)*param_3;
        param_3 = param_3 + 1;
      }
      local_1c = '\0';
      if (local_18 == '\0') {
        if ((*param_2 == 0x53) || (*param_2 == 0x43)) {
          local_18 = '\x01';
        }
        else {
          local_18 = -1;
        }
      }
      local_10 = *param_2 | 0x20;
      lVar9 = local_34;
      if (local_10 != 0x6e) {
        if ((local_10 == 99) || (local_10 == 0x7b)) {
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          lVar9 = local_34;
        }
        else {
          local_1dc = __whiteout(&local_24,param_1);
          lVar9 = local_34;
        }
      }
      local_34 = lVar9;
      if ((local_1ec != 0) && (local_20 == 0)) {
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        goto LAB__text__0058073a;
      }
      pbVar7 = param_2;
      switch(local_10) {
      case 99:
        if (local_1ec == 0) {
          local_1ec = 1;
          local_20 = local_20 + 1;
        }
        if ('\0' < local_18) {
          local_68 = local_68 + '\x01';
        }
        local_1e4 = &DAT_00764710;
        local_14 = local_14 - 1;
        goto LAB__text__0057f8d0;
      case 100:
      case 0x6f:
      case 0x75:
        goto switchD__text__0057f814_caseD_64;
      case 0x65:
      case 0x66:
      case 0x67:
        local_1e4 = &local_1d4;
        if (local_1dc == 0x2d) {
          local_1d4 = 0x2d;
          local_1e4 = local_1d3;
LAB__text__005801ff:
          local_20 = local_20 + -1;
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          lVar9 = local_34;
        }
        else if (local_1dc == 0x2b) goto LAB__text__005801ff;
        local_34 = lVar9;
        if ((local_1ec == 0) || (0x15d < local_20)) {
          local_20 = 0x15d;
        }
        while( true ) {
          if (DAT_00764370 < 2) {
            local_21c = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 4;
          }
          else {
            local_21c = FUN__text__0057bb50(local_1dc,4);
          }
          if ((local_21c == 0) ||
             (iVar4 = local_20 + -1, bVar8 = local_20 == 0, local_20 = iVar4, bVar8)) break;
          local_70 = local_70 + 1;
          *local_1e4 = (byte)local_1dc;
          local_1e4 = local_1e4 + 1;
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
        }
        if ((DAT_00764374 == (byte)local_1dc) &&
           (iVar4 = local_20 + -1, bVar8 = local_20 != 0, local_20 = iVar4, bVar8)) {
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          *local_1e4 = DAT_00764374;
          local_1e4 = local_1e4 + 1;
          while( true ) {
            if (DAT_00764370 < 2) {
              local_220 = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 4;
            }
            else {
              local_220 = FUN__text__0057bb50(local_1dc,4);
            }
            if ((local_220 == 0) ||
               (iVar4 = local_20 + -1, bVar8 = local_20 == 0, local_20 = iVar4, bVar8)) break;
            local_70 = local_70 + 1;
            *local_1e4 = (byte)local_1dc;
            local_1e4 = local_1e4 + 1;
            local_24 = local_24 + 1;
            local_1dc = __inc(param_1);
          }
        }
        if ((local_70 != 0) &&
           (((local_1dc == 0x65 || (local_1dc == 0x45)) &&
            (iVar4 = local_20 + -1, bVar8 = local_20 != 0, local_20 = iVar4, bVar8)))) {
          *local_1e4 = 0x65;
          local_1e4 = local_1e4 + 1;
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          if (local_1dc == 0x2d) {
            *local_1e4 = 0x2d;
            local_1e4 = local_1e4 + 1;
LAB__text__00580467:
            if (local_20 != 0) {
              local_24 = local_24 + 1;
              local_20 = local_20 + -1;
              local_1dc = __inc(param_1);
            }
          }
          else if (local_1dc == 0x2b) goto LAB__text__00580467;
          while( true ) {
            if (DAT_00764370 < 2) {
              local_224 = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 4;
            }
            else {
              local_224 = FUN__text__0057bb50(local_1dc,4);
            }
            if ((local_224 == 0) ||
               (iVar4 = local_20 + -1, bVar8 = local_20 == 0, local_20 = iVar4, bVar8)) break;
            local_70 = local_70 + 1;
            *local_1e4 = (byte)local_1dc;
            local_1e4 = local_1e4 + 1;
            local_24 = local_24 + 1;
            local_1dc = __inc(param_1);
          }
        }
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        if (local_70 == 0) goto LAB__text__0058073a;
        lVar9 = local_34;
        if (local_74 == '\0') {
          local_38 = local_38 + 1;
          *local_1e4 = 0;
          (*(code *)PTR_DAT_00761ba0)(local_3c + -1,local_40,&local_1d4);
          lVar9 = local_34;
        }
        break;
      default:
        if (*param_2 != local_1dc) {
          local_24 = local_24 - 1;
          FUN__text__005808f0(local_1dc,param_1);
          goto LAB__text__0058073a;
        }
        local_2c = local_2c + -1;
        if (local_74 == '\0') {
          param_3 = local_1d8;
        }
        break;
      case 0x69:
        local_10 = 100;
      case 0x78:
        if (local_1dc == 0x2d) {
          local_6c = local_6c + '\x01';
LAB__text__0057fc6f:
          local_20 = local_20 + -1;
          if ((local_20 == 0) && (local_1ec != 0)) {
            local_1c = local_1c + '\x01';
          }
          else {
            local_24 = local_24 + 1;
            local_1dc = __inc(param_1);
            lVar9 = local_34;
          }
        }
        else if (local_1dc == 0x2b) goto LAB__text__0057fc6f;
        local_34 = lVar9;
        if (local_1dc == 0x30) {
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          if (((byte)local_1dc == 'x') || ((byte)local_1dc == 'X')) {
            local_24 = local_24 + 1;
            local_1dc = __inc(param_1);
            local_10 = 0x78;
          }
          else {
            local_70 = local_70 + 1;
            if (local_10 == 0x78) {
              local_24 = local_24 - 1;
              FUN__text__005808f0(local_1dc,param_1);
              local_1dc = 0x30;
            }
            else {
              local_10 = 0x6f;
            }
          }
        }
        goto LAB__text__0057fdae;
      case 0x6e:
        local_44 = local_24;
        if (local_74 != '\0') break;
        goto LAB__text__00580171;
      case 0x70:
        local_3c = '\x01';
switchD__text__0057f814_caseD_64:
        if (local_1dc == 0x2d) {
          local_6c = local_6c + '\x01';
LAB__text__0057fd71:
          local_20 = local_20 + -1;
          if ((local_20 == 0) && (local_1ec != 0)) {
            local_1c = local_1c + '\x01';
          }
          else {
            local_24 = local_24 + 1;
            local_1dc = __inc(param_1);
          }
        }
        else if (local_1dc == 0x2b) goto LAB__text__0057fd71;
LAB__text__0057fdae:
        lVar9 = local_34;
        if (local_1e0 == 0) {
          while (local_1c == '\0') {
            local_34 = lVar9;
            if ((local_10 == 0x78) || (local_10 == 0x70)) {
              if (DAT_00764370 < 2) {
                local_214 = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 0x80;
              }
              else {
                local_214 = FUN__text__0057bb50(local_1dc,0x80);
                lVar9 = local_34;
              }
              if (local_214 == 0) {
                local_1c = local_1c + '\x01';
              }
              else {
                local_44 = local_44 << 4;
                local_34 = lVar9;
                local_1dc = FUN__text__00580830(local_1dc);
                lVar9 = local_34;
              }
            }
            else {
              if (DAT_00764370 < 2) {
                local_218 = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 4;
              }
              else {
                local_218 = FUN__text__0057bb50(local_1dc,4);
                lVar9 = local_34;
              }
              if (local_218 == 0) {
                local_1c = local_1c + '\x01';
              }
              else if (local_10 == 0x6f) {
                if ((int)local_1dc < 0x38) {
                  local_44 = local_44 << 3;
                }
                else {
                  local_1c = local_1c + '\x01';
                }
              }
              else {
                local_44 = local_44 * 10;
              }
            }
            local_34 = lVar9;
            if (local_1c == '\0') {
              local_70 = local_70 + 1;
              local_44 = (local_44 - 0x30) + local_1dc;
              if ((local_1ec == 0) || (local_20 = local_20 + -1, local_20 != 0)) {
                local_24 = local_24 + 1;
                local_1dc = __inc(param_1);
                lVar9 = local_34;
              }
              else {
                local_1c = '\x01';
              }
            }
            else {
              local_24 = local_24 - 1;
              FUN__text__005808f0(local_1dc,param_1);
              lVar9 = local_34;
            }
          }
          if (local_6c != '\0') {
            local_44 = -local_44;
          }
        }
        else {
          while( true ) {
            local_34._4_4_ = (int)((ulonglong)lVar9 >> 0x20);
            local_34._0_4_ = (int)lVar9;
            if (local_1c != '\0') break;
            local_34 = lVar9;
            if (local_10 == 0x78) {
              if (DAT_00764370 < 2) {
                local_20c = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 0x80;
              }
              else {
                local_20c = FUN__text__0057bb50(local_1dc,0x80);
              }
              if (local_20c == 0) {
                local_1c = local_1c + '\x01';
              }
              else {
                lVar9 = __allshl();
                local_34 = lVar9;
                local_1dc = FUN__text__00580830(local_1dc);
              }
            }
            else {
              if (DAT_00764370 < 2) {
                local_210 = *(ushort *)(PTR_DAT_00764164 + local_1dc * 2) & 4;
              }
              else {
                local_210 = FUN__text__0057bb50(local_1dc,4);
              }
              if (local_210 == 0) {
                local_1c = local_1c + '\x01';
              }
              else if (local_10 == 0x6f) {
                if ((int)local_1dc < 0x38) {
                  lVar9 = __allshl();
                  local_34 = lVar9;
                }
                else {
                  local_1c = local_1c + '\x01';
                }
              }
              else {
                __allshl();
                lVar9 = __allshl();
                local_34 = lVar9;
              }
            }
            if (local_1c == '\0') {
              local_70 = local_70 + 1;
              if ((local_1ec == 0) || (local_20 = local_20 + -1, local_20 != 0)) {
                local_24 = local_24 + 1;
                local_34 = local_34 + (int)(local_1dc - 0x30);
                local_1dc = __inc(param_1);
                lVar9 = local_34;
              }
              else {
                local_1c = '\x01';
                lVar9 = local_34 + (int)(local_1dc - 0x30);
              }
            }
            else {
              local_24 = local_24 - 1;
              FUN__text__005808f0(local_1dc,param_1);
              lVar9 = local_34;
            }
          }
          if (local_6c != '\0') {
            lVar9 = CONCAT44(-(local_34._4_4_ + (uint)((int)local_34 != 0)),-(int)local_34);
          }
        }
        if (local_10 == 0x46) {
          local_70 = 0;
        }
        if (local_70 == 0) goto LAB__text__0058073a;
        if (local_74 == '\0') {
          local_38 = local_38 + 1;
LAB__text__00580171:
          if (local_1e0 == 0) {
            if (local_3c == '\0') {
              *(undefined2 *)local_40 = (undefined2)local_44;
            }
            else {
              *local_40 = local_44;
            }
          }
          else {
            *(longlong *)local_40 = lVar9;
          }
        }
        break;
      case 0x73:
        if ('\0' < local_18) {
          local_68 = local_68 + '\x01';
        }
        local_1e4 = (byte *)0x764708;
        local_14 = local_14 - 1;
        goto LAB__text__0057f8d0;
      case 0x7b:
        if ('\0' < local_18) {
          local_68 = local_68 + '\x01';
        }
        pbVar7 = param_2 + 1;
        local_1e4 = pbVar7;
        if (*pbVar7 == 0x5e) {
          local_1e4 = param_2 + 2;
          local_14 = local_14 - 1;
        }
LAB__text__0057f8d0:
        param_2 = pbVar7;
        _memset(local_64,0,0x20);
        if ((local_10 == 0x7b) && (*local_1e4 == 0x5d)) {
          local_c = CONCAT31(local_c._1_3_,0x5d);
          local_59 = 0x20;
          local_1e4 = local_1e4 + 1;
        }
        while (*local_1e4 != 0x5d) {
          bVar1 = *local_1e4;
          local_1f0 = CONCAT31(local_1f0._1_3_,bVar1);
          pbVar7 = local_1e4 + 1;
          if (((bVar1 == 0x2d) && ((local_c & 0xff) != 0)) && (*pbVar7 != 0x5d)) {
            bVar1 = *pbVar7;
            local_1e4 = local_1e4 + 2;
            if ((uint)bVar1 <= (local_c & 0xff)) {
              bVar3 = (byte)local_c;
              local_c = CONCAT31(local_c._1_3_,bVar1);
              bVar1 = bVar3;
            }
            local_28 = CONCAT31(local_28._1_3_,bVar1);
            for (local_1f0 = CONCAT31(local_1f0._1_3_,(byte)local_c);
                (local_1f0 & 0xff) <= (local_28 & 0xff);
                local_1f0 = CONCAT31(local_1f0._1_3_,(byte)local_1f0 + 1)) {
              local_64[(int)(local_1f0 & 0xff) >> 3] =
                   local_64[(int)(local_1f0 & 0xff) >> 3] | (byte)(1 << ((byte)local_1f0 & 7));
            }
            local_c = local_c & 0xffffff00;
          }
          else {
            local_c = CONCAT31(local_c._1_3_,bVar1);
            local_64[(int)(uint)bVar1 >> 3] =
                 local_64[(int)(uint)bVar1 >> 3] | (byte)(1 << (bVar1 & 7));
            local_1e4 = pbVar7;
          }
        }
        if (*local_1e4 == 0) goto LAB__text__0058073a;
        if (local_10 == 0x7b) {
          param_2 = local_1e4;
        }
        local_1e8 = local_40;
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        while( true ) {
          if ((local_1ec != 0) &&
             (iVar4 = local_20 + -1, bVar8 = local_20 == 0, local_20 = iVar4, lVar9 = local_34,
             bVar8)) goto LAB__text__0057fc05;
          local_24 = local_24 + 1;
          local_1dc = __inc(param_1);
          if ((local_1dc == 0xffffffff) ||
             (bVar1 = (byte)local_1dc,
             ((int)(char)(local_64[(int)local_1dc >> 3] ^ local_14) & 1 << (bVar1 & 7)) == 0))
          break;
          if (local_74 == '\0') {
            if (local_68 == '\0') {
              *(byte *)local_40 = bVar1;
              local_40 = (uint *)((int)local_40 + 1);
            }
            else {
              local_1f4 = bVar1;
              if ((*(ushort *)(PTR_DAT_00764164 + (local_1dc & 0xff) * 2) & 0x8000) != 0) {
                local_24 = local_24 + 1;
                local_1f3 = __inc(param_1);
              }
              FUN__text__00589020(local_8,&local_1f4,DAT_00764370);
              *(undefined2 *)local_40 = local_8[0];
              local_40 = (uint *)((int)local_40 + 2);
            }
          }
          else {
            local_1e8 = (uint *)((int)local_1e8 + 1);
          }
        }
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        lVar9 = local_34;
LAB__text__0057fc05:
        if (local_1e8 == local_40) goto LAB__text__0058073a;
        if ((local_74 == '\0') && (local_38 = local_38 + 1, local_10 != 99)) {
          if (local_68 == '\0') {
            *(byte *)local_40 = 0;
          }
          else {
            *(undefined2 *)local_40 = 0;
          }
        }
      }
      local_2c = local_2c + '\x01';
      pbVar7 = param_2 + 1;
      local_34 = lVar9;
    }
    else {
      local_24 = local_24 + 1;
      bVar1 = *param_2;
      local_1dc = __inc(param_1);
      if (bVar1 != local_1dc) {
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        goto LAB__text__0058073a;
      }
      pbVar7 = param_2 + 1;
      if ((*(ushort *)(PTR_DAT_00764164 + (local_1dc & 0xff) * 2) & 0x8000) != 0) {
        local_24 = local_24 + 1;
        bVar1 = param_2[1];
        uVar6 = __inc(param_1);
        if (bVar1 == uVar6) {
          local_24 = local_24 - 1;
          pbVar7 = param_2 + 2;
          goto LAB__text__00580711;
        }
        local_24 = local_24 - 1;
        FUN__text__005808f0(uVar6,param_1);
        local_24 = local_24 - 1;
        FUN__text__005808f0(local_1dc,param_1);
        goto LAB__text__0058073a;
      }
    }
LAB__text__00580711:
    param_2 = pbVar7;
    if ((local_1dc == 0xffffffff) && ((*param_2 != 0x25 || (param_2[1] != 0x6e))))
    goto LAB__text__0058073a;
  } while( true );
}

