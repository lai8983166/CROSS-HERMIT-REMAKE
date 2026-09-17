
/* WARNING: Type propagation algorithm not settling */

int FUN_00575940(undefined4 param_1,byte *param_2,undefined4 *param_3)

{
  byte bVar1;
  code *pcVar2;
  ulonglong uVar3;
  byte *pbVar4;
  short sVar5;
  byte *pbVar6;
  uint uVar7;
  size_t sVar8;
  int iVar9;
  undefined2 extraout_var;
  short *psVar10;
  bool bVar11;
  ulonglong uVar12;
  longlong lVar13;
  int local_2a8;
  uint local_294;
  undefined1 local_28c [4];
  size_t local_288;
  short *local_284;
  int local_280;
  undefined8 local_27c;
  int local_274;
  undefined8 local_270;
  undefined4 local_268;
  undefined4 local_264;
  int *local_260;
  int local_25c;
  short *local_258;
  short *local_254;
  short *local_250;
  undefined2 local_24c;
  int local_248;
  undefined1 local_244;
  char local_243;
  int local_240;
  int local_23c;
  int local_238;
  int local_234;
  int local_230;
  short local_22c [255];
  undefined2 uStack_2d;
  undefined3 uStack_2b;
  size_t local_28;
  short *local_24;
  int local_20;
  int local_1c;
  undefined2 local_18;
  int local_14;
  uint local_10;
  undefined4 local_c;
  uint local_8;
  
  local_28 = 0;
  local_230 = 0;
  local_1c = 0;
  pbVar6 = param_2;
  do {
    param_2 = pbVar6;
    bVar1 = *param_2;
    stack0xffffffd4 = CONCAT31(uStack_2b,bVar1);
    pbVar6 = param_2 + 1;
    if ((bVar1 == 0) || (local_230 < 0)) {
      return local_230;
    }
    if (((char)bVar1 < ' ') || ('x' < (char)bVar1)) {
      local_294 = 0;
    }
    else {
      local_294 = (int)"(\"inconsistent IOB fields\", stream->_ptr - stream->_base >= 0)"
                       [(char)bVar1 + 0x2c] & 0xf;
    }
    local_10 = local_294;
    local_1c = (int)(char)(&DAT_005fa104)[local_294 * 8 + local_1c] >> 4;
    switch(local_1c) {
    case 0:
switchD_005759f9_caseD_0:
      local_20 = 0;
      pbVar4 = pbVar6;
      if ((*(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 0x8000) != 0) {
        FUN_00576670((int)(char)bVar1,param_1,&local_230);
        stack0xffffffd4 = CONCAT31(uStack_2b,*pbVar6);
        pbVar4 = param_2 + 2;
        if (*pbVar6 == 0) {
          iVar9 = FUN_00573780(2,"output.c",0x186,0,"ch != _T(\'\\0\')");
          if (iVar9 == 1) {
            pcVar2 = (code *)swi(3);
            iVar9 = (*pcVar2)();
            return iVar9;
          }
        }
      }
      param_2 = pbVar4;
      FUN_00576670((int)uStack_2d._1_1_,param_1,&local_230);
      pbVar6 = param_2;
      break;
    case 1:
      local_c = 0;
      local_240 = 0;
      local_248 = 0;
      local_14 = 0;
      local_8 = 0;
      local_238 = -1;
      local_20 = 0;
      break;
    case 2:
      switch(bVar1) {
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
      if (bVar1 == 0x2a) {
        local_248 = FUN_00576780(&param_3);
        if (local_248 < 0) {
          local_8 = local_8 | 4;
          local_248 = -local_248;
        }
      }
      else {
        local_248 = local_248 * 10 + -0x30 + (int)(char)bVar1;
      }
      break;
    case 4:
      local_238 = 0;
      break;
    case 5:
      if (bVar1 == 0x2a) {
        local_238 = FUN_00576780(&param_3);
        if (local_238 < 0) {
          local_238 = -1;
        }
      }
      else {
        local_238 = local_238 * 10 + -0x30 + (int)(char)bVar1;
      }
      break;
    case 6:
      switch(bVar1) {
      case 0x49:
        if ((*pbVar6 != 0x36) || (param_2[2] != 0x34)) {
          local_1c = 0;
          goto switchD_005759f9_caseD_0;
        }
        local_8 = local_8 | 0x8000;
        pbVar6 = param_2 + 3;
        break;
      case 0x68:
        local_8 = local_8 | 0x20;
        break;
      case 0x6c:
        local_8 = local_8 | 0x10;
        break;
      case 0x77:
        local_8 = local_8 | 0x800;
      }
      param_2 = pbVar6;
      pbVar6 = param_2;
      break;
    case 7:
      psVar10 = local_24;
      switch(bVar1) {
      case 0x43:
        if ((local_8 & 0x830) == 0) {
          local_8 = local_8 | 0x800;
        }
      case 99:
        if ((local_8 & 0x810) == 0) {
          local_24c = FUN_00576780(&param_3);
          local_22c[0]._0_1_ = (undefined1)local_24c;
          local_28 = 1;
        }
        else {
          local_18 = FUN_005767c0(&param_3);
          local_28 = FUN_00585ca0(local_22c,CONCAT22(extraout_var,local_18));
          if ((int)local_28 < 0) {
            local_240 = 1;
          }
        }
        psVar10 = local_22c;
        break;
      case 0x45:
      case 0x47:
        local_c = 1;
        stack0xffffffd4 = CONCAT31(uStack_2b,bVar1 + 0x20);
      case 0x65:
      case 0x66:
      case 0x67:
        local_8 = local_8 | 0x40;
        local_24 = local_22c;
        if (local_238 < 0) {
          local_238 = 6;
        }
        else if ((local_238 == 0) && (uStack_2d._1_1_ == 'g')) {
          local_238 = 1;
        }
        local_268 = *param_3;
        local_264 = param_3[1];
        param_3 = param_3 + 2;
        (*(code *)PTR_FUN_00761b98)(&local_268,local_24,(int)uStack_2d._1_1_,local_238,local_c);
        if (((local_8 & 0x80) != 0) && (local_238 == 0)) {
          (*(code *)PTR_FUN_00761ba4)(local_24);
        }
        if ((uStack_2d._1_1_ == 'g') && ((local_8 & 0x80) == 0)) {
          (*(code *)PTR_FUN_00761b9c)(local_24);
        }
        if ((char)*local_24 == '-') {
          local_8 = local_8 | 0x100;
          local_24 = (short *)((int)local_24 + 1);
        }
        local_28 = _strlen((char *)local_24);
        psVar10 = local_24;
        break;
      case 0x53:
        if ((local_8 & 0x830) == 0) {
          local_8 = local_8 | 0x800;
        }
      case 0x73:
        if (local_238 == -1) {
          local_2a8 = 0x7fffffff;
        }
        else {
          local_2a8 = local_238;
        }
        local_25c = local_2a8;
        local_24 = (short *)FUN_00576780(&param_3);
        if ((local_8 & 0x810) == 0) {
          if (local_24 == (short *)0x0) {
            local_24 = (short *)PTR_DAT_00761bc8;
          }
          for (local_254 = local_24; (local_25c != 0 && ((char)*local_254 != '\0'));
              local_254 = (short *)((int)local_254 + 1)) {
            local_25c = local_25c + -1;
          }
          local_28 = (int)local_254 - (int)local_24;
          local_25c = local_25c + -1;
          psVar10 = local_24;
        }
        else {
          if (local_24 == (short *)0x0) {
            local_24 = (short *)PTR_DAT_00761bcc;
          }
          local_20 = 1;
          for (local_258 = local_24; (local_25c != 0 && (*local_258 != 0));
              local_258 = local_258 + 1) {
            local_25c = local_25c + -1;
          }
          local_28 = (int)local_258 - (int)local_24 >> 1;
          local_25c = local_25c + -1;
          psVar10 = local_24;
        }
        break;
      case 0x5a:
        local_250 = (short *)FUN_00576780(&param_3);
        if ((local_250 == (short *)0x0) || (*(int *)(local_250 + 2) == 0)) {
          local_24 = (short *)PTR_DAT_00761bc8;
          local_28 = _strlen(PTR_DAT_00761bc8);
          psVar10 = local_24;
        }
        else if ((local_8 & 0x800) == 0) {
          local_20 = 0;
          local_28 = (size_t)*local_250;
          psVar10 = *(short **)(local_250 + 2);
        }
        else {
          local_28 = (uint)(int)*local_250 >> 1;
          local_20 = 1;
          psVar10 = *(short **)(local_250 + 2);
        }
        break;
      case 100:
      case 0x69:
        local_8 = local_8 | 0x40;
        local_23c = 10;
        goto LAB_00576105;
      case 0x6e:
        local_260 = (int *)FUN_00576780(&param_3);
        if ((local_8 & 0x20) == 0) {
          *local_260 = local_230;
        }
        else {
          *(undefined2 *)local_260 = (undefined2)local_230;
        }
        local_240 = 1;
        psVar10 = local_24;
        break;
      case 0x6f:
        local_23c = 8;
        if ((local_8 & 0x80) != 0) {
          local_8 = local_8 | 0x200;
        }
        goto LAB_00576105;
      case 0x70:
        local_238 = 8;
      case 0x58:
        local_234 = 7;
        goto LAB_005760af;
      case 0x75:
        local_23c = 10;
        goto LAB_00576105;
      case 0x78:
        local_234 = 0x27;
LAB_005760af:
        local_23c = 0x10;
        if ((local_8 & 0x80) != 0) {
          local_244 = 0x30;
          local_243 = (char)local_234 + 'Q';
          local_14 = 2;
        }
LAB_00576105:
        if ((local_8 & 0x8000) == 0) {
          if ((local_8 & 0x20) == 0) {
            if ((local_8 & 0x40) == 0) {
              uVar7 = FUN_00576780(&param_3);
              uVar12 = (ulonglong)uVar7;
            }
            else {
              iVar9 = FUN_00576780(&param_3);
              uVar12 = (ulonglong)iVar9;
            }
          }
          else if ((local_8 & 0x40) == 0) {
            uVar7 = FUN_00576780(&param_3);
            uVar12 = (ulonglong)(uVar7 & 0xffff);
          }
          else {
            sVar5 = FUN_00576780(&param_3);
            uVar12 = (ulonglong)(int)sVar5;
          }
        }
        else {
          uVar12 = FUN_005767a0(&param_3);
        }
        local_27c._4_4_ = (int)(uVar12 >> 0x20);
        local_27c._0_4_ = (int)uVar12;
        uVar3 = uVar12;
        if ((((local_8 & 0x40) != 0) && ((longlong)uVar12 < 0x100000000)) && ((longlong)uVar12 < 0))
        {
          local_8 = local_8 | 0x100;
          uVar3 = CONCAT44(-(local_27c._4_4_ + (uint)((int)local_27c != 0)),-(int)local_27c);
        }
        local_270._4_4_ = (int)(uVar3 >> 0x20);
        local_270._0_4_ = (int)uVar3;
        if ((local_8 & 0x8000) == 0) {
          local_270._4_4_ = 0;
        }
        lVar13 = CONCAT44(local_270._4_4_,(int)local_270);
        if (local_238 < 0) {
          local_238 = 1;
        }
        else {
          local_8 = local_8 & 0xfffffff7;
        }
        if ((int)local_270 == 0 && local_270._4_4_ == 0) {
          local_14 = 0;
        }
        local_24 = &uStack_2d;
        local_27c = uVar12;
        while ((iVar9 = local_238 + -1, 0 < local_238 || (lVar13 != 0))) {
          local_238 = iVar9;
          local_270 = lVar13;
          local_274 = __aullrem(lVar13,local_23c,local_23c >> 0x1f);
          local_274 = local_274 + 0x30;
          lVar13 = __aulldiv(local_270,local_23c,local_23c >> 0x1f);
          if (0x39 < local_274) {
            local_274 = local_274 + local_234;
          }
          *(char *)local_24 = (char)local_274;
          local_24 = (short *)((int)local_24 + -1);
        }
        local_28 = (int)&uStack_2d - (int)local_24;
        psVar10 = (short *)((int)local_24 + 1);
        local_270 = 0;
        local_238 = iVar9;
        if (((local_8 & 0x200) != 0) && ((*(char *)psVar10 != '0' || (local_28 == 0)))) {
          *(char *)local_24 = '0';
          local_28 = local_28 + 1;
          psVar10 = local_24;
        }
      }
      local_24 = psVar10;
      if (local_240 == 0) {
        if ((local_8 & 0x40) != 0) {
          if ((local_8 & 0x100) == 0) {
            if ((local_8 & 1) == 0) {
              if ((local_8 & 2) != 0) {
                local_244 = 0x20;
                local_14 = 1;
              }
            }
            else {
              local_244 = 0x2b;
              local_14 = 1;
            }
          }
          else {
            local_244 = 0x2d;
            local_14 = 1;
          }
        }
        local_280 = (local_248 - local_28) - local_14;
        if ((local_8 & 0xc) == 0) {
          FUN_005766f0(0x20,local_280,param_1,&local_230);
        }
        FUN_00576730(&local_244,local_14,param_1,&local_230);
        if (((local_8 & 8) != 0) && ((local_8 & 4) == 0)) {
          FUN_005766f0(0x30,local_280,param_1,&local_230);
        }
        if ((local_20 == 0) || ((int)local_28 < 1)) {
          FUN_00576730(local_24,local_28,param_1,&local_230);
        }
        else {
          local_284 = local_24;
          local_288 = local_28;
          while (sVar8 = local_288 - 1, bVar11 = local_288 != 0, local_288 = sVar8, bVar11) {
            sVar5 = *local_284;
            local_284 = local_284 + 1;
            iVar9 = FUN_00585ca0(local_28c,CONCAT22((short)(sVar8 >> 0x10),sVar5));
            if (iVar9 < 1) break;
            FUN_00576730(local_28c,iVar9,param_1,&local_230);
          }
        }
        if ((local_8 & 4) != 0) {
          FUN_005766f0(0x20,local_280,param_1,&local_230);
        }
      }
    }
  } while( true );
}

