
undefined4 FUN_0057a200(void)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  uint *puVar5;
  byte bVar6;
  uint *puVar7;
  int local_16c;
  uint local_15c;
  uint local_154;
  int local_150;
  uint local_14c;
  uint local_148;
  int local_144;
  uint *local_140;
  uint *local_138;
  uint *local_134;
  uint local_130;
  uint *local_12c;
  int local_124;
  uint local_120;
  int aiStack_11c [64];
  uint *local_1c;
  int local_18;
  uint *local_14;
  int local_10;
  uint *local_c;
  uint local_8;
  
  iVar3 = (*API_KERNEL32_DLL_IsBadWritePtr)(DAT_0080ab48,DAT_0080ab44 * 0x14);
  if (iVar3 == 0) {
    local_140 = DAT_0080ab48;
    for (local_124 = 0; local_124 < DAT_0080ab44; local_124 = local_124 + 1) {
      uVar1 = local_140[4];
      iVar3 = (*API_KERNEL32_DLL_IsBadWritePtr)(uVar1,0x41c4);
      if (iVar3 != 0) {
        return 0xfffffffe;
      }
      local_12c = (uint *)local_140[3];
      local_1c = (uint *)(uVar1 + 0x144);
      local_8 = local_140[2];
      local_148 = 0;
      local_15c = 0;
      for (local_10 = 0; local_10 < 0x20; local_10 = local_10 + 1) {
        local_120 = 0;
        local_154 = 0;
        local_130 = 0;
        for (local_150 = 0; local_150 < 0x40; local_150 = local_150 + 1) {
          aiStack_11c[local_150] = 0;
        }
        if (-1 < (int)local_8) {
          iVar3 = (*API_KERNEL32_DLL_IsBadWritePtr)(local_12c,0x8000);
          if (iVar3 != 0) {
            return 0xfffffffc;
          }
          local_c = local_12c;
          for (local_144 = 0; local_144 < 8; local_144 = local_144 + 1) {
            local_134 = local_c + 3;
            puVar7 = local_c + 0x3ff;
            if ((local_c[2] != 0xffffffff) || (*puVar7 != 0xffffffff)) {
              return 0xfffffffb;
            }
            do {
              uVar2 = *local_134;
              if ((uVar2 & 1) == 0) {
                local_150 = ((int)uVar2 >> 4) + -1;
                if (0x3f < local_150) {
                  local_150 = 0x3f;
                }
                aiStack_11c[local_150] = aiStack_11c[local_150] + 1;
                local_14c = uVar2;
              }
              else {
                if (0x400 < (int)(uVar2 - 1)) {
                  return 0xfffffffa;
                }
                local_130 = local_130 + 1;
                local_14c = uVar2 - 1;
              }
              if ((((int)local_14c < 0x10) || ((local_14c & 0xf) != 0)) || (0xff0 < (int)local_14c))
              {
                return 0xfffffff9;
              }
              if (*(uint *)((int)local_134 + (local_14c - 4)) != uVar2) {
                return 0xfffffff8;
              }
              local_134 = (uint *)((int)local_134 + local_14c);
            } while (local_134 < puVar7);
            if (local_134 != puVar7) {
              return 0xfffffff8;
            }
            local_c = local_c + 0x400;
          }
          if (*local_1c != local_130) {
            return 0xfffffff7;
          }
          local_138 = local_1c;
          for (local_18 = 0; local_18 < 0x40; local_18 = local_18 + 1) {
            local_134 = local_138;
            for (local_16c = 0;
                (puVar7 = (uint *)local_134[1], puVar7 != local_138 &&
                (local_16c != aiStack_11c[local_18])); local_16c = local_16c + 1) {
              if ((puVar7 < local_12c) || (local_12c + 0x2000 <= puVar7)) {
                return 0xfffffff6;
              }
              puVar5 = (uint *)(((uint)puVar7 & 0xfffff000) + 0xffc);
              for (local_14 = (uint *)(((uint)puVar7 & 0xfffff000) + 0xc);
                  (local_14 != puVar5 && (local_14 != puVar7));
                  local_14 = (uint *)((int)local_14 + (*local_14 & 0xfffffffe))) {
              }
              if (local_14 == puVar5) {
                return 0xfffffff5;
              }
              local_150 = ((int)*puVar7 >> 4) + -1;
              if (0x3f < local_150) {
                local_150 = 0x3f;
              }
              if (local_150 != local_18) {
                return 0xfffffff4;
              }
              if ((uint *)puVar7[2] != local_134) {
                return 0xfffffff3;
              }
              local_134 = puVar7;
            }
            if (local_16c != 0) {
              bVar6 = (byte)local_18;
              if (local_18 < 0x20) {
                local_120 = local_120 | 0x80000000U >> (bVar6 & 0x1f);
                local_148 = local_148 | 0x80000000U >> (bVar6 & 0x1f);
              }
              else {
                local_154 = local_154 | 0x80000000U >> (bVar6 - 0x20 & 0x1f);
                local_15c = local_15c | 0x80000000U >> (bVar6 - 0x20 & 0x1f);
              }
            }
            if (((uint *)local_134[1] != local_138) || (local_16c != aiStack_11c[local_18])) {
              return 0xfffffff2;
            }
            if ((uint *)local_138[2] != local_134) {
              return 0xfffffff1;
            }
            local_138 = local_138 + 2;
          }
        }
        if ((local_120 != *(uint *)(uVar1 + 0x44 + local_10 * 4)) ||
           (local_154 != *(uint *)(uVar1 + 0xc4 + local_10 * 4))) {
          return 0xfffffff0;
        }
        local_12c = local_12c + 0x2000;
        local_1c = local_1c + 0x81;
        local_8 = local_8 << 1;
      }
      if ((local_148 != *local_140) || (local_15c != local_140[1])) {
        return 0xffffffef;
      }
      local_140 = local_140 + 5;
    }
    uVar4 = 0;
  }
  else {
    uVar4 = 0xffffffff;
  }
  return uVar4;
}

