
int FUN__text__00582d30(undefined4 param_1,ushort *param_2,undefined4 *param_3)

{
  ushort uVar1;
  undefined2 uVar2;
  short sVar3;
  ushort *puVar4;
  uint uVar5;
  byte *pbVar6;
  int iVar7;
  undefined2 extraout_var;
  int iVar8;
  ulonglong uVar9;
  longlong lVar10;
  int local_4a4;
  uint local_490;
  byte *local_488;
  byte *local_484;
  int local_47c;
  int local_478;
  int local_474;
  int local_470;
  int local_46c;
  undefined4 local_468;
  undefined4 local_464;
  int *local_460;
  int local_45c;
  byte *local_458;
  byte *local_454;
  short *local_450;
  undefined1 local_44c;
  undefined1 local_44b;
  int local_448;
  undefined2 local_444;
  short local_442;
  int local_440;
  int local_43c;
  int local_438;
  int local_434;
  int local_430;
  undefined2 local_42c [255];
  byte local_22d [513];
  uint local_2c;
  byte *local_28;
  byte *local_24;
  int local_20;
  uint local_1c;
  undefined2 local_18 [2];
  int local_14;
  uint local_10;
  undefined4 local_c;
  uint local_8;
  
  local_28 = (byte *)0x0;
  local_430 = 0;
  local_1c = 0;
  puVar4 = param_2;
  do {
    param_2 = puVar4;
    uVar1 = *param_2;
    local_2c = CONCAT22(local_2c._2_2_,uVar1);
    puVar4 = param_2 + 1;
    if ((uVar1 == 0) || (local_430 < 0)) {
      return local_430;
    }
    if ((uVar1 < 0x20) || (0x78 < uVar1)) {
      local_490 = 0;
    }
    else {
      local_490 = (int)"(\"inconsistent IOB fields\", stream->_ptr - stream->_base >= 0)"
                       [uVar1 + 0x2c] & 0xf;
    }
    local_10 = local_490;
    local_1c = (int)(char)(&DAT_005fa104)[local_490 * 8 + local_1c] >> 4;
    uVar5 = local_1c;
    switch(local_1c) {
    case 0:
      goto switchD__text__00582dfb_caseD_0;
    case 1:
      local_c = 0;
      local_440 = 0;
      local_448 = 0;
      local_14 = 0;
      local_8 = 0;
      local_438 = -1;
      local_20 = 0;
      break;
    case 2:
      switch(uVar1) {
      case 0x20:
        local_8 = local_8 | 2;
        break;
      case 0x23:
        local_8 = local_8 | 0x80;
        break;
      case 0x2b:
        local_8 = local_8 | 1;
        break;
      case 0x2d:
        local_8 = local_8 | 4;
        break;
      case 0x30:
        local_8 = local_8 | 8;
      }
      break;
    case 3:
      if (uVar1 == 0x2a) {
        local_448 = FUN__text__00583ad0(&param_3);
        if (local_448 < 0) {
          local_8 = local_8 | 4;
          local_448 = -local_448;
        }
      }
      else {
        local_448 = local_448 * 10 + -0x30 + (uint)uVar1;
      }
      break;
    case 4:
      local_438 = 0;
      break;
    case 5:
      if (uVar1 == 0x2a) {
        local_438 = FUN__text__00583ad0(&param_3);
        if (local_438 < 0) {
          local_438 = -1;
        }
      }
      else {
        local_438 = local_438 * 10 + -0x30 + (uint)uVar1;
      }
      break;
    case 6:
      if (uVar1 == 0x49) {
        uVar5 = (uint)*puVar4;
        if ((uVar5 == 0x36) && (param_2[2] == 0x34)) {
          local_8 = local_8 | 0x8000;
          puVar4 = param_2 + 3;
        }
        else {
          local_1c = 0;
switchD__text__00582dfb_caseD_0:
          local_20 = 1;
          FUN__text__00583a00(CONCAT22((short)(uVar5 >> 0x10),uVar1),param_1,&local_430);
        }
      }
      else if (uVar1 == 0x68) {
        local_8 = local_8 | 0x20;
      }
      else if (uVar1 == 0x77) {
        local_8 = local_8 | 0x800;
      }
      break;
    case 7:
      pbVar6 = local_24;
      switch(uVar1) {
      case 0x43:
        if ((local_8 & 0x830) == 0) {
          local_8 = local_8 | 0x20;
        }
      case 99:
        local_20 = 1;
        uVar2 = FUN__text__00583ad0(&param_3);
        local_18[0] = uVar2;
        if ((local_8 & 0x20) != 0) {
          local_44c = (undefined1)uVar2;
          local_44b = 0;
          iVar8 = FUN__text__00589020(local_42c,&local_44c,DAT_00764370);
          uVar2 = local_42c[0];
          if (iVar8 < 0) {
            local_440 = 1;
          }
        }
        local_42c[0] = uVar2;
        local_28 = (byte *)0x1;
        pbVar6 = (byte *)local_42c;
        break;
      case 0x45:
      case 0x47:
        local_c = 1;
        local_2c = CONCAT22(local_2c._2_2_,uVar1 + 0x20);
      case 0x65:
      case 0x66:
      case 0x67:
        local_8 = local_8 | 0x40;
        local_24 = (byte *)local_42c;
        if (local_438 < 0) {
          local_438 = 6;
        }
        else if ((local_438 == 0) && ((local_2c & 0xffff) == 0x67)) {
          local_438 = 1;
        }
        local_468 = *param_3;
        local_464 = param_3[1];
        param_3 = param_3 + 2;
        (*(code *)PTR_FUN_00761b98)(&local_468,local_24,(int)(char)local_2c,local_438,local_c);
        if (((local_8 & 0x80) != 0) && (local_438 == 0)) {
          (*(code *)PTR_FUN_00761ba4)(local_24);
        }
        if (((local_2c & 0xffff) == 0x67) && ((local_8 & 0x80) == 0)) {
          (*(code *)PTR_FUN_00761b9c)(local_24);
        }
        if (*local_24 == 0x2d) {
          local_8 = local_8 | 0x100;
          local_24 = local_24 + 1;
        }
        local_28 = (byte *)_strlen((char *)local_24);
        pbVar6 = local_24;
        break;
      case 0x53:
        if ((local_8 & 0x830) == 0) {
          local_8 = local_8 | 0x20;
        }
      case 0x73:
        if (local_438 == -1) {
          local_4a4 = 0x7fffffff;
        }
        else {
          local_4a4 = local_438;
        }
        local_45c = local_4a4;
        local_24 = (byte *)FUN__text__00583ad0(&param_3);
        if ((local_8 & 0x20) == 0) {
          if (local_24 == (byte *)0x0) {
            local_24 = PTR_DAT_00761bcc;
          }
          local_20 = 1;
          for (local_458 = local_24; (local_45c != 0 && (*(short *)local_458 != 0));
              local_458 = local_458 + 2) {
            local_45c = local_45c + -1;
          }
          local_28 = (byte *)((int)local_458 - (int)local_24 >> 1);
          local_45c = local_45c + -1;
          pbVar6 = local_24;
        }
        else {
          if (local_24 == (byte *)0x0) {
            local_24 = PTR_DAT_00761bc8;
          }
          local_28 = (byte *)0x0;
          for (local_454 = local_24;
              (pbVar6 = local_24, (int)local_28 < local_45c && (*local_454 != 0));
              local_454 = local_454 + 1) {
            if ((*(ushort *)(PTR_DAT_00764164 + (uint)*local_454 * 2) & 0x8000) != 0) {
              local_454 = local_454 + 1;
            }
            local_28 = local_28 + 1;
          }
        }
        break;
      case 0x5a:
        local_450 = (short *)FUN__text__00583ad0(&param_3);
        if ((local_450 == (short *)0x0) || (*(int *)(local_450 + 2) == 0)) {
          local_24 = PTR_DAT_00761bc8;
          local_28 = (byte *)_strlen(PTR_DAT_00761bc8);
          pbVar6 = local_24;
        }
        else if ((local_8 & 0x800) == 0) {
          local_20 = 0;
          local_28 = (byte *)(int)*local_450;
          pbVar6 = *(byte **)(local_450 + 2);
        }
        else {
          local_28 = (byte *)((uint)(int)*local_450 >> 1);
          local_20 = 1;
          pbVar6 = *(byte **)(local_450 + 2);
        }
        break;
      case 100:
      case 0x69:
        local_8 = local_8 | 0x40;
        local_43c = 10;
        goto LAB__text__005834e5;
      case 0x6e:
        local_460 = (int *)FUN__text__00583ad0(&param_3);
        if ((local_8 & 0x20) == 0) {
          *local_460 = local_430;
        }
        else {
          *(undefined2 *)local_460 = (undefined2)local_430;
        }
        local_440 = 1;
        pbVar6 = local_24;
        break;
      case 0x6f:
        local_43c = 8;
        if ((local_8 & 0x80) != 0) {
          local_8 = local_8 | 0x200;
        }
        goto LAB__text__005834e5;
      case 0x70:
        local_438 = 8;
      case 0x58:
        local_434 = 7;
        goto LAB__text__0058348d;
      case 0x75:
        local_43c = 10;
        goto LAB__text__005834e5;
      case 0x78:
        local_434 = 0x27;
LAB__text__0058348d:
        local_43c = 0x10;
        if ((local_8 & 0x80) != 0) {
          local_444 = 0x30;
          local_442 = (short)local_434 + 0x51;
          local_14 = 2;
        }
LAB__text__005834e5:
        if ((local_8 & 0x8000) == 0) {
          if ((local_8 & 0x20) == 0) {
            if ((local_8 & 0x40) == 0) {
              uVar5 = FUN__text__00583ad0(&param_3);
              uVar9 = (ulonglong)uVar5;
            }
            else {
              iVar8 = FUN__text__00583ad0(&param_3);
              uVar9 = (ulonglong)iVar8;
            }
          }
          else if ((local_8 & 0x40) == 0) {
            uVar5 = FUN__text__00583ad0(&param_3);
            uVar9 = (ulonglong)(uVar5 & 0xffff);
          }
          else {
            sVar3 = FUN__text__00583ad0(&param_3);
            uVar9 = (ulonglong)(int)sVar3;
          }
        }
        else {
          uVar9 = FUN__text__00583af0(&param_3);
        }
        local_478 = (int)(uVar9 >> 0x20);
        local_47c = (int)uVar9;
        if ((((local_8 & 0x40) != 0) && ((longlong)uVar9 < 0x100000000)) && ((longlong)uVar9 < 0)) {
          uVar9 = CONCAT44(-(local_478 + (uint)(local_47c != 0)),-local_47c);
          local_8 = local_8 | 0x100;
        }
        local_46c = (int)(uVar9 >> 0x20);
        local_470 = (int)uVar9;
        if ((local_8 & 0x8000) == 0) {
          local_46c = 0;
        }
        lVar10 = CONCAT44(local_46c,local_470);
        if (local_438 < 0) {
          local_438 = 1;
        }
        else {
          local_8 = local_8 & 0xfffffff7;
        }
        if (local_470 == 0 && local_46c == 0) {
          local_14 = 0;
        }
        local_24 = local_22d;
        while ((iVar8 = local_438 + -1, 0 < local_438 || (lVar10 != 0))) {
          local_438 = iVar8;
          local_474 = __aullrem(lVar10,local_43c,local_43c >> 0x1f);
          local_474 = local_474 + 0x30;
          lVar10 = __aulldiv(lVar10,local_43c,local_43c >> 0x1f);
          if (0x39 < local_474) {
            local_474 = local_474 + local_434;
          }
          *local_24 = (byte)local_474;
          local_24 = local_24 + -1;
        }
        local_28 = local_22d + -(int)local_24;
        pbVar6 = local_24 + 1;
        local_438 = iVar8;
        if (((local_8 & 0x200) != 0) && ((*pbVar6 != 0x30 || (local_28 == (byte *)0x0)))) {
          *local_24 = 0x30;
          local_28 = local_28 + 1;
          pbVar6 = local_24;
        }
      }
      local_24 = pbVar6;
      if (local_440 == 0) {
        if ((local_8 & 0x40) != 0) {
          if ((local_8 & 0x100) == 0) {
            if ((local_8 & 1) == 0) {
              if ((local_8 & 2) != 0) {
                local_444 = 0x20;
                local_14 = 1;
              }
            }
            else {
              local_444 = 0x2b;
              local_14 = 1;
            }
          }
          else {
            local_444 = 0x2d;
            local_14 = 1;
          }
        }
        iVar8 = (local_448 - (int)local_28) - local_14;
        if ((local_8 & 0xc) == 0) {
          write_multi_char(0x20,iVar8,param_1,&local_430);
        }
        FUN__text__00583a80(&local_444,local_14,param_1,&local_430);
        if (((local_8 & 8) != 0) && ((local_8 & 4) == 0)) {
          write_multi_char(0x30,iVar8,param_1,&local_430);
        }
        if ((local_20 == 0) && (0 < (int)local_28)) {
          local_484 = local_24;
          local_488 = local_28;
          while ((0 < (int)local_488 &&
                 (iVar7 = FUN__text__00589020(local_18,local_484,DAT_00764370), 0 < iVar7))) {
            FUN__text__00583a00(CONCAT22(extraout_var,local_18[0]),param_1,&local_430);
            local_484 = local_484 + iVar7;
            local_488 = local_488 + -1;
          }
        }
        else {
          FUN__text__00583a80(local_24,local_28,param_1,&local_430);
        }
        if ((local_8 & 4) != 0) {
          write_multi_char(0x20,iVar8,param_1,&local_430);
        }
      }
    }
  } while( true );
}

