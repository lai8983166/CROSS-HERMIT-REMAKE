
uint FUN__text__0058b6f0(undefined2 *param_1,undefined4 *param_2,byte *param_3,undefined4 param_4,
                        int param_5,int param_6,int param_7)

{
  byte bVar1;
  bool bVar2;
  byte *pbVar3;
  uint local_b4;
  uint local_b0;
  uint local_a4;
  uint local_9c;
  uint local_94;
  int local_80;
  int local_78;
  uint local_74;
  int local_70;
  char *local_6c;
  byte *local_68;
  undefined2 local_64;
  undefined4 local_62;
  undefined4 local_5e;
  ushort local_5a;
  int local_58;
  ushort local_54;
  int local_50;
  undefined2 local_4c;
  uint local_48;
  int local_44;
  uint local_40;
  char local_3c [23];
  char local_25;
  undefined4 local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  undefined4 local_c;
  byte *local_8;
  
  local_6c = local_3c;
  local_20 = local_20 & 0xffff0000;
  local_78 = 1;
  local_74 = 0;
  local_58 = 0;
  local_10 = 0;
  local_1c = 0;
  local_44 = 0;
  bVar2 = false;
  local_18 = 0;
  local_70 = 0;
  local_48 = 0;
  local_50 = 0;
  local_68 = param_3;
  for (local_8 = param_3;
      (((*local_8 == 0x20 || (*local_8 == 9)) || (*local_8 == 10)) || (*local_8 == 0xd));
      local_8 = local_8 + 1) {
  }
  do {
    if (local_50 == 10) {
      *param_2 = local_8;
      if ((local_58 != 0) && (local_44 == 0)) {
        if (0x18 < local_74) {
          if ('\x04' < local_25) {
            local_25 = local_25 + '\x01';
          }
          local_74 = 0x18;
          local_6c = local_6c + -1;
          local_70 = local_70 + 1;
        }
        if (local_74 == 0) {
          local_4c = 0;
          local_54 = 0;
          local_14 = 0;
          local_c = 0;
        }
        else {
          while (local_6c = local_6c + -1, *local_6c == '\0') {
            local_74 = local_74 - 1;
            local_70 = local_70 + 1;
          }
          FUN__text__0058b5b0(local_3c,local_74,&local_64);
          if (local_78 < 0) {
            local_18 = -local_18;
          }
          local_18 = local_18 + local_70;
          if (local_1c == 0) {
            local_18 = local_18 + param_5;
          }
          if (local_10 == 0) {
            local_18 = local_18 - param_6;
          }
          if (local_18 < 0x1451) {
            if (local_18 < -0x1450) {
              bVar2 = true;
            }
            else {
              FUN__text__0058dc20(&local_64,local_18,param_4);
              local_4c = local_64;
              local_c = local_62;
              local_14 = local_5e;
              local_54 = local_5a;
            }
          }
          else {
            local_44 = 1;
          }
        }
      }
      if (local_58 == 0) {
        local_4c = 0;
        local_54 = 0;
        local_14 = 0;
        local_c = 0;
        local_48 = local_48 | 4;
      }
      else if (local_44 == 0) {
        if (bVar2) {
          local_4c = 0;
          local_54 = 0;
          local_14 = 0;
          local_c = 0;
          local_48 = local_48 | 1;
        }
      }
      else {
        local_54 = 0x7fff;
        local_14 = 0x80000000;
        local_c = 0;
        local_4c = 0;
        local_48 = local_48 | 2;
      }
      *param_1 = local_4c;
      *(undefined4 *)(param_1 + 1) = local_c;
      *(undefined4 *)(param_1 + 3) = local_14;
      param_1[5] = local_54 | (ushort)local_20;
      return local_48;
    }
    bVar1 = *local_8;
    local_40 = CONCAT31(local_40._1_3_,bVar1);
    pbVar3 = local_8 + 1;
    switch(local_50) {
    case 0:
      if (((char)bVar1 < '1') || ('9' < (char)bVar1)) {
        if (bVar1 == DAT_00764374) {
          local_50 = 5;
        }
        else if (bVar1 == 0x2b) {
          local_50 = 2;
          local_20 = (uint)local_20._2_2_ << 0x10;
        }
        else if (bVar1 == 0x2d) {
          local_50 = 2;
          local_20 = CONCAT22(local_20._2_2_,0x8000);
        }
        else if (bVar1 == 0x30) {
          local_50 = 1;
        }
        else {
          local_50 = 10;
          pbVar3 = local_8;
        }
      }
      else {
        local_50 = 3;
        pbVar3 = local_8;
      }
      break;
    case 1:
      local_58 = 1;
      if (((char)bVar1 < '1') || ('9' < (char)bVar1)) {
        if (bVar1 == DAT_00764374) {
          local_50 = 4;
        }
        else {
          switch(bVar1) {
          case 0x2b:
          case 0x2d:
            local_50 = 0xb;
            pbVar3 = local_8;
            break;
          default:
            local_50 = 10;
            pbVar3 = local_8;
            break;
          case 0x30:
            local_50 = 1;
            break;
          case 0x44:
          case 0x45:
          case 100:
          case 0x65:
            local_50 = 6;
          }
        }
      }
      else {
        local_50 = 3;
        pbVar3 = local_8;
      }
      break;
    case 2:
      if (((char)bVar1 < '1') || ('9' < (char)bVar1)) {
        if (bVar1 == DAT_00764374) {
          local_50 = 5;
        }
        else if (bVar1 == 0x30) {
          local_50 = 1;
        }
        else {
          local_50 = 10;
          local_8 = local_68;
          pbVar3 = local_8;
        }
      }
      else {
        local_50 = 3;
        pbVar3 = local_8;
      }
      break;
    case 3:
      local_58 = 1;
      local_8 = pbVar3;
      while( true ) {
        if (DAT_00764370 < 2) {
          local_94 = *(ushort *)(PTR_DAT_00764164 + (local_40 & 0xff) * 2) & 4;
        }
        else {
          local_94 = FUN__text__0057bb50(local_40 & 0xff,4);
        }
        if (local_94 == 0) break;
        if (local_74 < 0x19) {
          local_74 = local_74 + 1;
          *local_6c = (char)local_40 + -0x30;
          local_6c = local_6c + 1;
        }
        else {
          local_70 = local_70 + 1;
        }
        local_40 = CONCAT31(local_40._1_3_,*local_8);
        local_8 = local_8 + 1;
      }
      pbVar3 = local_8;
      if ((char)local_40 == DAT_00764374) {
        local_50 = 4;
      }
      else {
        switch((char)local_40) {
        case '+':
        case '-':
          local_50 = 0xb;
          pbVar3 = local_8 + -1;
          break;
        default:
          local_50 = 10;
          pbVar3 = local_8 + -1;
          break;
        case 'D':
        case 'E':
        case 'd':
        case 'e':
          local_50 = 6;
        }
      }
      break;
    case 4:
      local_58 = 1;
      local_10 = 1;
      local_8 = pbVar3;
      if (local_74 == 0) {
        while ((char)local_40 == '0') {
          local_70 = local_70 + -1;
          local_40 = CONCAT31(local_40._1_3_,*local_8);
          local_8 = local_8 + 1;
        }
      }
      while( true ) {
        if (DAT_00764370 < 2) {
          local_9c = *(ushort *)(PTR_DAT_00764164 + (local_40 & 0xff) * 2) & 4;
        }
        else {
          local_9c = FUN__text__0057bb50(local_40 & 0xff,4);
        }
        if (local_9c == 0) break;
        if (local_74 < 0x19) {
          local_74 = local_74 + 1;
          *local_6c = (char)local_40 + -0x30;
          local_6c = local_6c + 1;
          local_70 = local_70 + -1;
        }
        local_40 = CONCAT31(local_40._1_3_,*local_8);
        local_8 = local_8 + 1;
      }
      switch((char)local_40) {
      case '+':
      case '-':
        local_50 = 0xb;
        pbVar3 = local_8 + -1;
        break;
      default:
        local_50 = 10;
        pbVar3 = local_8 + -1;
        break;
      case 'D':
      case 'E':
      case 'd':
      case 'e':
        local_50 = 6;
        pbVar3 = local_8;
      }
      break;
    case 5:
      local_10 = 1;
      if (DAT_00764370 < 2) {
        local_a4 = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 4;
        local_8 = pbVar3;
      }
      else {
        local_8 = pbVar3;
        local_a4 = FUN__text__0057bb50(bVar1,4);
      }
      if (local_a4 == 0) {
        local_50 = 10;
        local_8 = local_68;
        pbVar3 = local_8;
      }
      else {
        local_50 = 4;
        pbVar3 = local_8 + -1;
      }
      break;
    case 6:
      local_68 = local_8 + -1;
      if (((char)bVar1 < '1') || ('9' < (char)bVar1)) {
        if (bVar1 == 0x2b) {
          local_50 = 7;
        }
        else if (bVar1 == 0x2d) {
          local_50 = 7;
          local_78 = -1;
        }
        else if (bVar1 == 0x30) {
          local_50 = 8;
        }
        else {
          local_50 = 10;
          pbVar3 = local_68;
        }
      }
      else {
        local_50 = 9;
        pbVar3 = local_8;
      }
      break;
    case 7:
      if (((char)bVar1 < '1') || ('9' < (char)bVar1)) {
        if (bVar1 == 0x30) {
          local_50 = 8;
        }
        else {
          local_50 = 10;
          local_8 = local_68;
          pbVar3 = local_8;
        }
      }
      else {
        local_50 = 9;
        pbVar3 = local_8;
      }
      break;
    case 8:
      local_1c = 1;
      local_8 = pbVar3;
      while ((char)local_40 == '0') {
        bVar1 = *local_8;
        local_8 = local_8 + 1;
        local_40 = CONCAT31(local_40._1_3_,bVar1);
      }
      if (((char)local_40 < '1') || ('9' < (char)local_40)) {
        local_50 = 10;
      }
      else {
        local_50 = 9;
      }
      local_8 = local_8 + -1;
      pbVar3 = local_8;
      break;
    case 9:
      local_1c = 1;
      local_80 = 0;
      local_8 = pbVar3;
      while( true ) {
        if (DAT_00764370 < 2) {
          local_b0 = *(ushort *)(PTR_DAT_00764164 + (local_40 & 0xff) * 2) & 4;
        }
        else {
          local_b0 = FUN__text__0057bb50(local_40 & 0xff,4);
        }
        if (local_b0 == 0) goto LAB__text__0058be17;
        local_80 = local_80 * 10 + -0x30 + (int)(char)local_40;
        if (0x1450 < local_80) break;
        local_40 = CONCAT31(local_40._1_3_,*local_8);
        local_8 = local_8 + 1;
      }
      local_80 = 0x1451;
LAB__text__0058be17:
      local_18 = local_80;
      while( true ) {
        if (DAT_00764370 < 2) {
          local_b4 = *(ushort *)(PTR_DAT_00764164 + (local_40 & 0xff) * 2) & 4;
        }
        else {
          local_b4 = FUN__text__0057bb50(local_40 & 0xff,4);
        }
        if (local_b4 == 0) break;
        local_40 = CONCAT31(local_40._1_3_,*local_8);
        local_8 = local_8 + 1;
      }
      local_50 = 10;
      pbVar3 = local_8 + -1;
      break;
    case 0xb:
      if (param_7 == 0) {
        local_50 = 10;
        pbVar3 = local_8;
      }
      else {
        local_68 = local_8;
        if (bVar1 == 0x2b) {
          local_50 = 7;
        }
        else if (bVar1 == 0x2d) {
          local_50 = 7;
          local_78 = -1;
        }
        else {
          local_50 = 10;
          pbVar3 = local_8;
        }
      }
    }
    local_8 = pbVar3;
  } while( true );
}

