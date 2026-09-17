
void __fastcall FUN__text__004a7d30(undefined4 param_1)

{
  undefined4 *puVar1;
  int iVar2;
  short asStackY_70058 [6];
  undefined2 auStackY_7004c [229286];
  undefined4 local_ec [16];
  int local_ac;
  uint local_a8;
  int local_a4;
  int local_a0;
  uint local_9c;
  undefined1 local_98 [16];
  undefined1 local_88 [16];
  ushort local_78;
  short local_74;
  short local_70;
  ushort local_6c;
  short local_68;
  undefined4 local_64;
  uint local_60;
  uint local_5c;
  short asStack_58 [2];
  undefined4 auStack_54 [2];
  undefined2 auStack_4c [30];
  undefined1 local_10;
  short local_c;
  undefined4 local_8;
  
  puVar1 = local_ec;
  for (iVar2 = 0x3a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar1 = 0xcccccccc;
    puVar1 = puVar1 + 1;
  }
  local_8 = param_1;
  local_10 = 0;
  local_5c = local_5c & 0xffff0000;
  local_9c = (uint)DAT_007a55fa;
  if (local_9c == 0) {
    local_60 = local_60 & 0xffff0000;
    local_64 = CONCAT22(local_64._2_2_,1);
    iVar2 = 0;
    for (local_c = 0; local_c < 5; local_c = local_c + 1) {
      puVar1 = (undefined4 *)
               FUN__text__004a95f0(local_88,CONCAT22((short)((uint)iVar2 >> 0x10),local_c));
      iVar2 = (int)local_c;
      *(undefined4 *)(asStack_58 + iVar2 * 7) = *puVar1;
      *(undefined4 *)((int)auStack_54 + iVar2 * 0xe) = puVar1[1];
      *(undefined4 *)((int)auStack_54 + iVar2 * 0xe + 4) = puVar1[2];
      auStack_4c[iVar2 * 7] = *(undefined2 *)(puVar1 + 3);
      iVar2 = (int)asStack_58[local_c * 7];
      local_a0 = iVar2;
      switch(iVar2) {
      case 0:
        break;
      case 1:
      case 3:
      case 5:
        local_60 = CONCAT22(local_60._2_2_,1);
        local_64 = (uint)local_64._2_2_ << 0x10;
        break;
      case 2:
        local_5c = CONCAT22(local_5c._2_2_,1);
        local_64 = (uint)local_64._2_2_ << 0x10;
        iVar2 = 0;
        break;
      case 4:
        local_64 = (uint)local_64._2_2_ << 0x10;
        break;
      default:
        goto switchD__text__004a7e0b_default;
      }
      if ((local_60 & 0xffff) != 0) goto switchD__text__004a7e0b_default;
    }
    if (((local_64 & 0xffff) != 0) || ((local_5c & 0xffff) == 0))
    goto switchD__text__004a7e0b_default;
  }
  else {
    if (local_9c != 1) goto switchD__text__004a7e0b_default;
    for (local_c = 0; local_c < 5; local_c = local_c + 1) {
      puVar1 = (undefined4 *)FUN__text__004a95f0(local_98,local_c);
      iVar2 = (int)local_c;
      *(undefined4 *)(asStack_58 + iVar2 * 7) = *puVar1;
      *(undefined4 *)((int)auStack_54 + iVar2 * 0xe) = puVar1[1];
      *(undefined4 *)((int)auStack_54 + iVar2 * 0xe + 4) = puVar1[2];
      auStack_4c[iVar2 * 7] = *(undefined2 *)(puVar1 + 3);
      local_a4 = (int)asStack_58[local_c * 7];
      if (local_a4 != 0) {
        if (local_a4 != 2) goto switchD__text__004a7e0b_default;
        local_5c = CONCAT22(local_5c._2_2_,1);
      }
    }
  }
  if ((local_5c & 0xffff) != 0) {
    local_68 = DAT_007aab16;
    local_6c = (ushort)(byte)(&DAT_0073bedf)[DAT_007aab16 * 0x100];
    for (local_70 = 0; local_70 < (short)(ushort)(byte)(&DAT_0073bedf)[DAT_007aab16 * 0x100];
        local_70 = local_70 + 1) {
      for (local_74 = 0; local_74 < 5; local_74 = local_74 + 1) {
        local_a8 = (uint)(*(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) & 0x7ff);
        if ((*(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) & 0x7ff) == 2) {
          local_78 = 0;
          local_ac = (int)local_74;
          switch((int)local_74) {
          case 0:
            local_78 = *(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) >> 0xb & 1;
            break;
          case 1:
            local_78 = *(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) >> 0xc & 1;
            break;
          case 2:
            local_78 = *(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) >> 0xd & 1;
            break;
          case 3:
            local_78 = *(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) >> 0xe & 1;
            break;
          case 4:
            local_78 = *(ushort *)(&DAT_0073bee2 + local_70 * 4 + DAT_007aab16 * 0x100) >> 0xf;
          }
          if ((local_78 != 0) && (asStack_58[local_74 * 7] != 2))
          goto switchD__text__004a7e0b_default;
        }
      }
    }
  }
switchD__text__004a7e0b_default:
  local_8 = 0x4a8104;
  FUN__text__0056ce80();
  return;
}

