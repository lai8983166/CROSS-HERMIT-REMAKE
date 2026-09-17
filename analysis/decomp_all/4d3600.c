
void FUN__text__004d3600(int *param_1,short param_2,short param_3,short param_4)

{
  undefined4 *puVar1;
  int iVar2;
  int *piVar3;
  undefined4 *puVar4;
  undefined4 local_1d8 [16];
  int local_198;
  undefined1 local_194 [32];
  undefined4 local_174;
  undefined2 local_170;
  int local_16c;
  undefined4 local_168 [6];
  int local_150;
  int local_148;
  int local_144;
  int local_140;
  int local_13c;
  int local_138;
  undefined1 local_134 [12];
  int local_128;
  int local_3c [7];
  int local_20;
  undefined *local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar1 = local_1d8;
  for (iVar2 = 0x75; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar1 = 0xcccccccc;
    puVar1 = puVar1 + 1;
  }
  local_10 = 0;
  local_14 = 0;
  local_18 = 0;
  local_1c = &DAT_007e17e8 + param_2 * 0x4a0;
  FUN__text__004d58e0(local_134,param_2);
  for (local_c = 0; local_c < 7; local_c = local_c + 1) {
    if (*(short *)(&DAT_0074befc + local_c * 2 + param_3 * 0x60) != 0) {
      local_14 = local_14 + (ushort)(byte)local_1c[local_c * 8 + 0xc];
      local_18 = local_18 + 1;
    }
  }
  if (local_10 != 0) {
    local_10 = local_14 / local_18;
  }
  local_13c = 0;
  local_140 = 0;
  local_144 = 0;
  for (local_c = 0; local_c < 8; local_c = local_c + 1) {
    local_138 = *(int *)(&DAT_0074bedc + local_c * 4 + param_3 * 0x60);
    if (0 < local_138) {
      local_138 = (((local_138 * (param_4 + 0x32)) / 100) * (local_10 + 0x32)) / 100;
    }
    iVar2 = local_138;
    local_198 = (int)local_c;
    if (local_198 == 7) {
      local_20 = local_138;
    }
    else {
      local_140 = local_13c;
      local_13c = local_13c + local_138;
      local_148 = local_128 - local_13c;
      if (local_148 < 0) {
        local_148 = local_138 + local_148;
        if (local_148 < 0) {
          local_138 = 0;
        }
        else {
          iVar2 = local_138 - local_148;
          local_138 = local_148;
        }
        local_144 = local_144 + iVar2 / 2;
      }
      else {
        local_170 = 0;
        local_174 = 0;
        local_16c = local_138;
        puVar1 = (undefined4 *)
                 FUN__text__004d56a0(local_194,
                                     CONCAT22((short)((uint)*(undefined4 *)
                                                             (&DAT_007e17f8 +
                                                             local_c * 8 + param_2 * 0x4a0) >> 0x10)
                                              ,(ushort)(byte)(&DAT_007e17f4)
                                                             [local_c * 8 + param_2 * 0x4a0]),
                                     *(undefined4 *)(&DAT_007e17f8 + local_c * 8 + param_2 * 0x4a0))
        ;
        puVar4 = local_168;
        for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar1;
          puVar1 = puVar1 + 1;
          puVar4 = puVar4 + 1;
        }
        if (local_150 < local_16c) {
          local_144 = local_144 + (local_16c - local_150) / 2;
          local_16c = local_150;
        }
        local_138 = local_16c;
      }
      local_3c[local_c] = local_138;
    }
  }
  local_20 = local_20 + local_144;
  piVar3 = local_3c;
  for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
    *param_1 = *piVar3;
    piVar3 = piVar3 + 1;
    param_1 = param_1 + 1;
  }
  local_8 = 0x4d394c;
  FUN__text__0056ce80();
  return;
}

