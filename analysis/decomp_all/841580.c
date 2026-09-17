
uint FUN__text1__00841580(uint param_1,byte *param_2,uint param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  uint local_14;
  uint local_10;
  uint local_c;
  uint local_8;
  
  local_8 = param_1 & 0xffff;
  local_c = param_1 >> 0x10;
  if (param_2 == (byte *)0x0) {
    local_8 = 1;
  }
  else {
    while (param_3 != 0) {
      if (param_3 < 0x15b0) {
        local_14 = param_3;
      }
      else {
        local_14 = 0x15b0;
      }
      param_3 = param_3 - local_14;
      for (local_10 = local_14; 0xf < (int)local_10; local_10 = local_10 - 0x10) {
        iVar6 = local_8 + *param_2;
        iVar11 = iVar6 + (uint)param_2[1];
        iVar1 = iVar11 + (uint)param_2[2];
        iVar7 = iVar1 + (uint)param_2[3];
        iVar12 = iVar7 + (uint)param_2[4];
        iVar2 = iVar12 + (uint)param_2[5];
        iVar8 = iVar2 + (uint)param_2[6];
        iVar13 = iVar8 + (uint)param_2[7];
        iVar3 = iVar13 + (uint)param_2[8];
        iVar9 = iVar3 + (uint)param_2[9];
        iVar14 = iVar9 + (uint)param_2[10];
        iVar4 = iVar14 + (uint)param_2[0xb];
        iVar10 = iVar4 + (uint)param_2[0xc];
        iVar15 = iVar10 + (uint)param_2[0xd];
        iVar5 = iVar15 + (uint)param_2[0xe];
        local_8 = iVar5 + (uint)param_2[0xf];
        local_c = local_c + iVar6 + iVar11 + iVar1 + iVar7 + iVar12 + iVar2 + iVar8 + iVar13 + iVar3
                  + iVar9 + iVar14 + iVar4 + iVar10 + iVar15 + iVar5 + local_8;
        param_2 = param_2 + 0x10;
      }
      for (; local_10 != 0; local_10 = local_10 - 1) {
        local_8 = local_8 + *param_2;
        param_2 = param_2 + 1;
        local_c = local_c + local_8;
      }
      local_8 = local_8 % 0xfff1;
      local_c = local_c % 0xfff1;
    }
    local_8 = local_c << 0x10 | local_8;
  }
  return local_8;
}

