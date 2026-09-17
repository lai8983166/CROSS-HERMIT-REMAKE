
int FUN__text1__00849a03(undefined4 param_1,byte *param_2,undefined4 *param_3)

{
  byte *pbVar1;
  short sVar2;
  uint uVar3;
  short *psVar4;
  short *psVar5;
  undefined4 uVar6;
  int *piVar7;
  int iVar8;
  byte bVar9;
  int iVar10;
  undefined1 *puVar11;
  ulonglong uVar12;
  longlong lVar13;
  undefined1 local_24c [511];
  undefined1 local_4d;
  undefined4 local_4c;
  undefined4 local_48;
  int local_44;
  int local_40;
  undefined1 local_3c [4];
  undefined4 local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  undefined1 local_1a;
  char local_19;
  int local_18;
  int local_14;
  undefined1 *local_10;
  short *local_c;
  uint local_8;
  
  local_34 = 0;
  bVar9 = *param_2;
  local_10 = (undefined1 *)0x0;
  local_18 = 0;
  pbVar1 = param_2;
  do {
    if ((bVar9 == 0) || (param_2 = pbVar1 + 1, local_18 < 0)) {
      return local_18;
    }
    if (((char)bVar9 < ' ') || ('x' < (char)bVar9)) {
      uVar3 = 0;
    }
    else {
      uVar3 = (byte)(&DAT_00873f74)[(char)bVar9] & 0xf;
    }
    local_34 = (int)(char)(&DAT_00873f94)[uVar3 * 8 + local_34] >> 4;
    switch(local_34) {
    case 0:
switchD__text1__00849a71_caseD_0:
      local_28 = 0;
      if ((PTR_DAT_00870260[(uint)bVar9 * 2 + 1] & 0x80) != 0) {
        FUN__text1__0084a144((int)(char)bVar9,param_1,&local_18);
        bVar9 = *param_2;
        param_2 = pbVar1 + 2;
      }
      FUN__text1__0084a144((int)(char)bVar9,param_1,&local_18);
      break;
    case 1:
      local_14 = -1;
      local_38 = 0;
      local_2c = 0;
      local_24 = 0;
      local_20 = 0;
      local_8 = 0;
      local_28 = 0;
      break;
    case 2:
      if (bVar9 == 0x20) {
        local_8 = local_8 | 2;
      }
      else if (bVar9 == 0x23) {
        local_8 = local_8 | 0x80;
      }
      else if (bVar9 == 0x2b) {
        local_8 = local_8 | 1;
      }
      else if (bVar9 == 0x2d) {
        local_8 = local_8 | 4;
      }
      else if (bVar9 == 0x30) {
        local_8 = local_8 | 8;
      }
      break;
    case 3:
      if (bVar9 == 0x2a) {
        local_24 = FUN__text1__0084a1e2(&param_3);
        if (local_24 < 0) {
          local_8 = local_8 | 4;
          local_24 = -local_24;
        }
      }
      else {
        local_24 = (char)bVar9 + -0x30 + local_24 * 10;
      }
      break;
    case 4:
      local_14 = 0;
      break;
    case 5:
      if (bVar9 == 0x2a) {
        local_14 = FUN__text1__0084a1e2(&param_3);
        if (local_14 < 0) {
          local_14 = -1;
        }
      }
      else {
        local_14 = (char)bVar9 + -0x30 + local_14 * 10;
      }
      break;
    case 6:
      if (bVar9 == 0x49) {
        if ((*param_2 != 0x36) || (pbVar1[2] != 0x34)) {
          local_34 = 0;
          goto switchD__text1__00849a71_caseD_0;
        }
        param_2 = pbVar1 + 3;
        local_8 = local_8 | 0x8000;
      }
      else if (bVar9 == 0x68) {
        local_8 = local_8 | 0x20;
      }
      else if (bVar9 == 0x6c) {
        local_8 = local_8 | 0x10;
      }
      else if (bVar9 == 0x77) {
        local_8 = local_8 | 0x800;
      }
      break;
    case 7:
      psVar5 = local_c;
      if ((char)bVar9 < 'h') {
        if ((char)bVar9 < 'e') {
          if ((char)bVar9 < 'Y') {
            if (bVar9 == 0x58) {
LAB__text1__00849e82:
              local_30 = 7;
LAB__text1__00849e89:
              local_10 = (undefined1 *)0x10;
              if ((local_8 & 0x80) != 0) {
                local_1a = 0x30;
                local_19 = (char)local_30 + 'Q';
                local_20 = 2;
              }
              goto LAB__text1__00849ef3;
            }
            if (bVar9 != 0x43) {
              if ((bVar9 != 0x45) && (bVar9 != 0x47)) {
                if (bVar9 == 0x53) {
                  if ((local_8 & 0x830) == 0) {
                    local_8 = local_8 | 0x800;
                  }
                  goto LAB__text1__00849c30;
                }
                goto LAB__text1__0084a00d;
              }
              local_38 = 1;
              bVar9 = bVar9 + 0x20;
              goto LAB__text1__00849c91;
            }
            if ((local_8 & 0x830) == 0) {
              local_8 = local_8 | 0x800;
            }
LAB__text1__00849cbe:
            if ((local_8 & 0x810) == 0) {
              local_24c[0] = FUN__text1__0084a1e2(&param_3);
              local_10 = (undefined1 *)0x1;
            }
            else {
              uVar6 = FUN__text1__0084a1ff();
              local_10 = (undefined1 *)FUN__text1__0084c421(local_24c,uVar6);
              if ((int)local_10 < 0) {
                local_2c = 1;
              }
            }
            psVar5 = (short *)local_24c;
          }
          else if (bVar9 == 0x5a) {
            psVar4 = (short *)FUN__text1__0084a1e2(&param_3);
            if ((psVar4 == (short *)0x0) ||
               (psVar5 = *(short **)(psVar4 + 2), psVar5 == (short *)0x0)) {
              local_c = (short *)PTR_DAT_00870258;
              psVar5 = (short *)PTR_DAT_00870258;
              goto LAB__text1__00849e03;
            }
            if ((local_8 & 0x800) == 0) {
              local_28 = 0;
              local_10 = (undefined1 *)(int)*psVar4;
            }
            else {
              local_28 = 1;
              local_10 = (undefined1 *)((uint)(int)*psVar4 >> 1);
            }
          }
          else {
            if (bVar9 == 99) goto LAB__text1__00849cbe;
            if (bVar9 == 100) goto LAB__text1__00849ee8;
          }
        }
        else {
LAB__text1__00849c91:
          local_8 = local_8 | 0x40;
          psVar5 = (short *)local_24c;
          if (local_14 < 0) {
            local_14 = 6;
          }
          else if ((local_14 == 0) && (bVar9 == 0x67)) {
            local_14 = 1;
          }
          local_4c = *param_3;
          local_48 = param_3[1];
          param_3 = param_3 + 2;
          local_c = psVar5;
          (*(code *)PTR_DAT_00872850)(&local_4c,local_24c,(int)(char)bVar9,local_14,local_38);
          uVar3 = local_8 & 0x80;
          if ((uVar3 != 0) && (local_14 == 0)) {
            (*(code *)PTR_DAT_0087285c)(local_24c);
          }
          if ((bVar9 == 0x67) && (uVar3 == 0)) {
            (*(code *)PTR_DAT_00872854)(local_24c);
          }
          if (local_24c[0] == '-') {
            local_8 = local_8 | 0x100;
            psVar5 = (short *)(local_24c + 1);
            local_c = psVar5;
          }
LAB__text1__00849e03:
          local_10 = (undefined1 *)_strlen((char *)psVar5);
          psVar5 = local_c;
        }
      }
      else {
        if (bVar9 == 0x69) {
LAB__text1__00849ee8:
          local_8 = local_8 | 0x40;
        }
        else {
          if (bVar9 == 0x6e) {
            piVar7 = (int *)FUN__text1__0084a1e2(&param_3);
            if ((local_8 & 0x20) == 0) {
              *piVar7 = local_18;
            }
            else {
              *(undefined2 *)piVar7 = (undefined2)local_18;
            }
            local_2c = 1;
            break;
          }
          if (bVar9 == 0x6f) {
            local_10 = (undefined1 *)0x8;
            if ((local_8 & 0x80) != 0) {
              local_8 = local_8 | 0x200;
            }
            goto LAB__text1__00849ef3;
          }
          if (bVar9 == 0x70) {
            local_14 = 8;
            goto LAB__text1__00849e82;
          }
          if (bVar9 == 0x73) {
LAB__text1__00849c30:
            iVar10 = local_14;
            if (local_14 == -1) {
              iVar10 = 0x7fffffff;
            }
            psVar4 = (short *)FUN__text1__0084a1e2(&param_3);
            if ((local_8 & 0x810) == 0) {
              psVar5 = psVar4;
              if (psVar4 == (short *)0x0) {
                psVar4 = (short *)PTR_DAT_00870258;
                psVar5 = (short *)PTR_DAT_00870258;
              }
              for (; (iVar10 != 0 && ((char)*psVar4 != '\0')); psVar4 = (short *)((int)psVar4 + 1))
              {
                iVar10 = iVar10 + -1;
              }
              local_10 = (undefined1 *)((int)psVar4 - (int)psVar5);
            }
            else {
              if (psVar4 == (short *)0x0) {
                psVar4 = (short *)PTR_DAT_0087025c;
              }
              local_28 = 1;
              for (psVar5 = psVar4; (iVar10 != 0 && (*psVar5 != 0)); psVar5 = psVar5 + 1) {
                iVar10 = iVar10 + -1;
              }
              local_10 = (undefined1 *)((int)psVar5 - (int)psVar4 >> 1);
              psVar5 = psVar4;
            }
            goto LAB__text1__0084a00d;
          }
          if (bVar9 != 0x75) {
            if (bVar9 != 0x78) goto LAB__text1__0084a00d;
            local_30 = 0x27;
            goto LAB__text1__00849e89;
          }
        }
        local_10 = (undefined1 *)0xa;
LAB__text1__00849ef3:
        if ((local_8 & 0x8000) == 0) {
          if ((local_8 & 0x20) == 0) {
            if ((local_8 & 0x40) == 0) {
              uVar3 = FUN__text1__0084a1e2(&param_3);
              uVar12 = (ulonglong)uVar3;
              goto LAB__text1__00849f46;
            }
            uVar3 = FUN__text1__0084a1e2(&param_3);
          }
          else if ((local_8 & 0x40) == 0) {
            uVar3 = FUN__text1__0084a1e2(&param_3);
            uVar3 = uVar3 & 0xffff;
          }
          else {
            sVar2 = FUN__text1__0084a1e2(&param_3);
            uVar3 = (uint)sVar2;
          }
          uVar12 = (ulonglong)(int)uVar3;
        }
        else {
          uVar12 = FUN__text1__0084a1ef(&param_3);
        }
LAB__text1__00849f46:
        if ((((local_8 & 0x40) != 0) && ((longlong)uVar12 < 0x100000000)) && ((longlong)uVar12 < 0))
        {
          uVar12 = CONCAT44(-((int)(uVar12 >> 0x20) + (uint)((int)uVar12 != 0)),-(int)uVar12);
          local_8 = local_8 | 0x100;
        }
        iVar10 = (int)(uVar12 >> 0x20);
        if ((local_8 & 0x8000) == 0) {
          iVar10 = 0;
        }
        lVar13 = CONCAT44(iVar10,(int)uVar12);
        if (local_14 < 0) {
          local_14 = 1;
        }
        else {
          local_8 = local_8 & 0xfffffff7;
        }
        if ((int)uVar12 == 0 && iVar10 == 0) {
          local_20 = 0;
        }
        local_c = (short *)&local_4d;
        while ((iVar10 = local_14 + -1, 0 < local_14 || (lVar13 != 0))) {
          local_40 = (int)local_10 >> 0x1f;
          local_44 = (int)local_10;
          local_14 = iVar10;
          iVar10 = __aullrem(lVar13,local_10,local_40);
          iVar10 = iVar10 + 0x30;
          lVar13 = __aulldiv(lVar13,local_44,local_40);
          if (0x39 < iVar10) {
            iVar10 = iVar10 + local_30;
          }
          psVar5 = (short *)((int)local_c + -1);
          *(char *)local_c = (char)iVar10;
          local_c = psVar5;
        }
        iVar8 = -(int)local_c;
        local_10 = &local_4d + iVar8;
        psVar5 = (short *)((int)local_c + 1);
        local_14 = iVar10;
        if (((local_8 & 0x200) != 0) &&
           ((*(char *)psVar5 != '0' || (local_10 == (undefined1 *)0x0)))) {
          *(char *)local_c = '0';
          local_10 = (undefined1 *)((int)&local_4c + iVar8);
          psVar5 = local_c;
        }
      }
LAB__text1__0084a00d:
      local_c = psVar5;
      uVar3 = local_8;
      if (local_2c == 0) {
        if ((local_8 & 0x40) != 0) {
          if ((local_8 & 0x100) == 0) {
            if ((local_8 & 1) == 0) {
              if ((local_8 & 2) == 0) goto LAB__text1__0084a045;
              local_1a = 0x20;
            }
            else {
              local_1a = 0x2b;
            }
          }
          else {
            local_1a = 0x2d;
          }
          local_20 = 1;
        }
LAB__text1__0084a045:
        iVar10 = (local_24 - local_20) - (int)local_10;
        if ((local_8 & 0xc) == 0) {
          FUN__text1__0084a179(0x20,iVar10,param_1,&local_18);
        }
        FUN__text1__0084a1aa(&local_1a,local_20,param_1,&local_18);
        if (((uVar3 & 8) != 0) && ((uVar3 & 4) == 0)) {
          FUN__text1__0084a179(0x30,iVar10,param_1,&local_18);
        }
        if ((local_28 == 0) || (puVar11 = local_10, psVar5 = local_c, (int)local_10 < 1)) {
          FUN__text1__0084a1aa(local_c,local_10,param_1,&local_18);
        }
        else {
          do {
            puVar11 = puVar11 + -1;
            iVar8 = FUN__text1__0084c421(local_3c,*psVar5);
            if (iVar8 < 1) break;
            FUN__text1__0084a1aa(local_3c,iVar8,param_1,&local_18);
            psVar5 = psVar5 + 1;
          } while (puVar11 != (undefined1 *)0x0);
        }
        if ((local_8 & 4) != 0) {
          FUN__text1__0084a179(0x20,iVar10,param_1,&local_18);
        }
      }
    }
    bVar9 = *param_2;
    pbVar1 = param_2;
  } while( true );
}

