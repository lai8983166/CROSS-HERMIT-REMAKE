
undefined4
FUN__text1__00847068
          (int *param_1,uint param_2,uint param_3,int param_4,int param_5,uint *param_6,
          uint *param_7,int param_8,int *param_9,uint *param_10)

{
  uint uVar1;
  uint uVar2;
  char cVar3;
  undefined3 uVar4;
  byte bVar5;
  int iVar6;
  uint uVar7;
  undefined4 local_10c;
  uint local_108;
  uint local_104;
  uint local_100;
  uint local_fc;
  uint local_f8;
  uint local_f4;
  uint local_f0;
  int local_ec;
  int local_e8;
  uint local_e4 [16];
  uint local_a4;
  int local_a0;
  uint *local_9c;
  uint local_98 [16];
  uint local_58 [16];
  undefined4 local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  uint *local_8;
  
  local_58[0] = 0;
  local_58[1] = 0;
  local_58[2] = 0;
  local_58[3] = 0;
  local_58[4] = 0;
  local_58[5] = 0;
  local_58[6] = 0;
  local_58[7] = 0;
  local_58[8] = 0;
  local_58[9] = 0;
  local_58[10] = 0;
  local_58[0xb] = 0;
  local_58[0xc] = 0;
  local_58[0xd] = 0;
  local_58[0xe] = 0;
  local_58[0xf] = 0;
  local_8 = (uint *)param_1;
  local_f0 = param_2;
  do {
    local_58[*local_8] = local_58[*local_8] + 1;
    local_8 = local_8 + 1;
    local_f0 = local_f0 - 1;
  } while (local_f0 != 0);
  if (local_58[0] == param_2) {
    *param_6 = 0;
    *param_7 = 0;
    local_10c = 0;
  }
  else {
    local_104 = *param_7;
    for (local_f8 = 1; (local_f8 < 0x10 && (local_58[local_f8] == 0)); local_f8 = local_f8 + 1) {
    }
    local_100 = local_f8;
    if (local_104 < local_f8) {
      local_104 = local_f8;
    }
    for (local_f0 = 0xf; (local_f0 != 0 && (local_58[local_f0] == 0)); local_f0 = local_f0 - 1) {
    }
    local_a4 = local_f0;
    if (local_f0 < local_104) {
      local_104 = local_f0;
    }
    *param_7 = local_104;
    local_ec = 1 << ((byte)local_f8 & 0x1f);
    for (; local_f8 < local_f0; local_f8 = local_f8 + 1) {
      if ((int)(local_ec - local_58[local_f8]) < 0) {
        return 0xfffffffd;
      }
      local_ec = (local_ec - local_58[local_f8]) * 2;
    }
    local_ec = local_ec - local_58[local_f0];
    if (local_ec < 0) {
      local_10c = 0xfffffffd;
    }
    else {
      local_58[local_f0] = local_58[local_f0] + local_ec;
      local_f8 = 0;
      local_e4[1] = 0;
      local_8 = local_58;
      local_9c = local_e4 + 2;
      while( true ) {
        local_8 = local_8 + 1;
        local_f0 = local_f0 - 1;
        if (local_f0 == 0) break;
        local_f8 = local_f8 + *local_8;
        *local_9c = local_f8;
        local_9c = local_9c + 1;
      }
      local_8 = (uint *)param_1;
      local_f0 = 0;
      do {
        iVar6 = *local_8;
        local_8 = local_8 + 1;
        if (iVar6 != 0) {
          param_10[local_e4[iVar6]] = local_f0;
          local_e4[iVar6] = local_e4[iVar6] + 1;
        }
        local_f0 = local_f0 + 1;
      } while (local_f0 < param_2);
      uVar1 = local_e4[local_a4];
      local_f0 = 0;
      local_e4[0] = 0;
      local_8 = param_10;
      local_e8 = -1;
      local_a0 = -local_104;
      local_98[1] = 0;
      local_c = 0;
      local_f4 = 0;
      for (; (int)local_100 <= (int)local_a4; local_100 = local_100 + 1) {
        local_10 = local_58[local_100];
        while (uVar2 = local_10, local_10 = local_10 - 1, uVar2 != 0) {
          while ((int)(local_a0 + local_104) < (int)local_100) {
            iVar6 = local_e8 + 1;
            local_a0 = local_a0 + local_104;
            local_108 = local_a4 - local_a0;
            if (local_104 < local_108) {
              local_108 = local_104;
            }
            local_f8 = local_100 - local_a0;
            local_98[0] = 1 << ((byte)local_f8 & 0x1f);
            if (local_10 + 1 < local_98[0]) {
              local_98[0] = local_98[0] - (local_10 + 1);
              local_9c = local_58 + local_100;
              if (local_f8 < local_108) {
                while (local_f8 = local_f8 + 1, local_f8 < local_108) {
                  local_98[0] = local_98[0] * 2;
                  local_9c = local_9c + 1;
                  if (local_98[0] <= *local_9c) break;
                  local_98[0] = local_98[0] - *local_9c;
                }
              }
            }
            local_f4 = 1 << ((byte)local_f8 & 0x1f);
            if (0x5a0 < *param_9 + local_f4) {
              return 0xfffffffd;
            }
            local_c = param_8 + *param_9 * 8;
            local_98[local_e8 + 2] = local_c;
            *param_9 = *param_9 + local_f4;
            local_e8 = iVar6;
            if (iVar6 == 0) {
              *param_6 = local_c;
            }
            else {
              local_e4[iVar6] = local_f0;
              local_18 = CONCAT31(CONCAT21(local_18._2_2_,(char)local_104),(byte)local_f8);
              uVar7 = local_f0 >> ((char)local_a0 - (char)local_104 & 0x1fU);
              local_14 = ((int)(local_c - local_98[iVar6]) >> 3) - uVar7;
              uVar2 = local_98[iVar6];
              *(undefined4 *)(uVar2 + uVar7 * 8) = local_18;
              *(uint *)(uVar2 + 4 + uVar7 * 8) = local_14;
            }
          }
          bVar5 = (byte)local_a0;
          cVar3 = (char)local_100;
          uVar4 = CONCAT21(local_18._2_2_,cVar3 - bVar5);
          if (local_8 < param_10 + uVar1) {
            if (*local_8 < param_3) {
              local_18 = CONCAT31(uVar4,(-(*local_8 < 0x100) & 0xa0U) + 0x60);
              local_14 = *local_8;
              local_8 = local_8 + 1;
            }
            else {
              local_18 = CONCAT31(uVar4,(char)*(undefined4 *)(param_5 + (*local_8 - param_3) * 4) +
                                        'P');
              local_14 = *(uint *)(param_4 + (*local_8 - param_3) * 4);
              local_8 = local_8 + 1;
            }
          }
          else {
            local_18 = CONCAT31(uVar4,0xc0);
          }
          local_98[0] = 1 << (cVar3 - bVar5 & 0x1f);
          for (local_f8 = local_f0 >> (bVar5 & 0x1f); local_f8 < local_f4;
              local_f8 = local_f8 + local_98[0]) {
            *(undefined4 *)(local_c + local_f8 * 8) = local_18;
            *(uint *)(local_c + 4 + local_f8 * 8) = local_14;
          }
          local_f8 = 1 << (cVar3 - 1U & 0x1f);
          while ((local_f0 & local_f8) != 0) {
            local_f0 = local_f0 ^ local_f8;
            local_f8 = local_f8 >> 1;
          }
          local_f0 = local_f0 ^ local_f8;
          for (; local_fc = (1 << (bVar5 & 0x1f)) - 1, (local_f0 & local_fc) != local_e4[local_e8];
              local_e8 = local_e8 + -1) {
            local_a0 = local_a0 - local_104;
            bVar5 = (byte)local_a0;
          }
        }
      }
      if ((local_ec == 0) || (local_a4 == 1)) {
        local_10c = 0;
      }
      else {
        local_10c = 0xfffffffb;
      }
    }
  }
  return local_10c;
}

