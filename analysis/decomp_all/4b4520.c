
void __thiscall FUN__text__004b4520(int param_1,uint param_2)

{
  int iVar1;
  ushort uVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_80 [16];
  int local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined *local_34;
  uint local_30;
  uint local_2c;
  undefined *local_28;
  ushort local_24;
  undefined2 uStack_22;
  short local_20;
  short local_1c;
  ushort local_18;
  uint local_14;
  undefined *local_10;
  undefined4 local_c;
  int local_8;
  
  puVar4 = local_80;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = local_14 & 0xffff0000;
  uVar2 = *(ushort *)(param_1 + 0x596 + DAT_007d6a34 * 2);
  _local_24 = CONCAT22(uStack_22,uVar2);
  local_28 = &DAT_007e17e8 + (uint)uVar2 * 0x4a0;
  local_20 = 0;
  local_8 = param_1;
  while( true ) {
    if (2 < local_20) break;
    local_18 = 0xffff;
    local_1c = (short)(char)(&DAT_006d514d)[(int)local_20 + (param_2 & 0xffff) * 0x38];
    local_40 = local_1c + -8;
    switch(local_40) {
    case 0:
      local_18 = *(ushort *)(&DAT_006d5124 + (param_2 & 0xffff) * 0x38);
      break;
    case 1:
      local_18 = *(ushort *)(&DAT_006d5126 + (param_2 & 0xffff) * 0x38);
      break;
    case 2:
      local_18 = *(ushort *)(&DAT_006d5128 + (param_2 & 0xffff) * 0x38);
      break;
    case 3:
      local_18 = *(ushort *)(&DAT_006d512a + (param_2 & 0xffff) * 0x38);
      break;
    case 4:
      local_18 = *(ushort *)(&DAT_006d512c + (param_2 & 0xffff) * 0x38);
      break;
    case 5:
      local_18 = *(ushort *)(&DAT_006d512e + (param_2 & 0xffff) * 0x38);
      break;
    case 6:
      local_18 = (ushort)(byte)(&DAT_006d5130)[(param_2 & 0xffff) * 0x38];
      break;
    case 7:
      local_18 = *(ushort *)(&DAT_006d5132 + (param_2 & 0xffff) * 0x38);
      break;
    case 8:
      local_18 = (ushort)(byte)(&DAT_006d5134)[(param_2 & 0xffff) * 0x38];
      break;
    case 9:
      local_18 = (ushort)(byte)(&DAT_006d5135)[(param_2 & 0xffff) * 0x38];
      break;
    case 10:
      local_18 = (ushort)(byte)(&DAT_006d5136)[(param_2 & 0xffff) * 0x38];
      break;
    case 0xb:
      local_18 = (ushort)(byte)(&DAT_006d5137)[(param_2 & 0xffff) * 0x38];
      break;
    case 0xc:
      local_18 = (ushort)(byte)(&DAT_006d5138)[(param_2 & 0xffff) * 0x38];
      break;
    case 0xd:
      local_18 = (ushort)(byte)(&DAT_006d5139)[(param_2 & 0xffff) * 0x38];
      break;
    case 0xe:
      local_18 = *(ushort *)(&DAT_006d513a + (param_2 & 0xffff) * 0x38);
      break;
    case 0xf:
      local_18 = *(ushort *)(&DAT_006d513c + (param_2 & 0xffff) * 0x38);
      break;
    case 0x10:
      local_18 = *(ushort *)(&DAT_006d513e + (param_2 & 0xffff) * 0x38);
      break;
    case 0x11:
      local_18 = (ushort)(byte)(&DAT_006d5140)[(param_2 & 0xffff) * 0x38];
      break;
    case 0x12:
      local_18 = *(ushort *)(&DAT_006d5144 + (param_2 & 0xffff) * 0x38);
      break;
    case 0x13:
      local_18 = *(ushort *)(&DAT_006d5148 + (param_2 & 0xffff) * 0x38);
      break;
    case 0x14:
      local_18 = *(ushort *)(&DAT_006d514a + (param_2 & 0xffff) * 0x38);
      break;
    case 0x15:
      local_18 = (ushort)(byte)(&DAT_006d514c)[(param_2 & 0xffff) * 0x38];
    }
    if (-1 < (short)local_18) {
      local_10 = &DAT_0061bf90;
      FUN__text__004d2790(&DAT_0061bf90,1,0x4a,0x2ae,(local_14 & 0xffff) * 0x13 + 0x22c,0,
                          (local_1c + -8) * 0x10);
      if (local_1c == 0x19) {
        local_10 = &DAT_0061bfb0;
        FUN__text__004d2790(&DAT_0061bfb0,1,0x4a,0x2ea,(local_14 & 0xffff) * 0x13 + 0x22e,0,
                            ((short)local_18 + -1) * 0x10);
      }
      else {
        FUN__text__004b7230(0x300,(local_14 & 0xffff) * 0x13 + 0x22e,0,0,2,0x4a,0x3f,
                            (int)(short)local_18,1);
      }
      local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
    }
    local_20 = local_20 + 1;
  }
  uVar3 = (int)((param_2 & 0xffff) - 1) % 0xc;
  local_2c = CONCAT22(local_2c._2_2_,(short)uVar3);
  if (8 < (uVar3 & 0xffff)) {
    local_2c = CONCAT22(local_2c._2_2_,8);
  }
  local_10 = &DAT_0061bfc0;
  FUN__text__004d2790(&DAT_0061bfc0,1,0x4a,0x394,0x1ed,0,(local_2c & 0xffff) * 0xe);
  local_30._0_2_ = *(ushort *)(&DAT_006d511a + (param_2 & 0xffff) * 0x38);
  local_34 = &DAT_006e45f8;
  FUN__text__004b7230(0x3b1,0x200,0,0,2,0x4a,0x3f,(&DAT_006e45f8)[(ushort)local_30],1);
  local_38 = (uint)local_38._2_2_ << 0x10;
  local_30 = CONCAT22(local_30._2_2_,*(undefined2 *)(&DAT_006d511a + (param_2 & 0xffff) * 0x38));
  local_10 = &DAT_0061bfd0;
  local_3c = (uint)local_3c._2_2_ << 0x10;
  local_c = (uint)local_c._2_2_ << 0x10;
  while ((local_c & 0xffff) < 5) {
    local_38 = CONCAT22(local_38._2_2_,1);
    uVar2 = (ushort)(byte)local_28[0x72] + (short)local_c * 2;
    local_3c = CONCAT22(local_3c._2_2_,uVar2);
    if ((&DAT_006e45f8)[(local_30 & 0xffff) + (uint)uVar2 * 0xf] != '\0') {
      local_38 = (uint)local_38._2_2_ << 0x10;
    }
    FUN__text__004d2790(local_10,1,0x4a,0x3be,(local_c & 0xffff) * 0x13 + 0x22f,0,
                        (local_38 & 0xffff) * 0xe);
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4b4a9f;
  FUN__text__0056ce80();
  return;
}

