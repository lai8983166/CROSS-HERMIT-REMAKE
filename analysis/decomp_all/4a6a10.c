
void __fastcall FUN__text__004a6a10(undefined4 param_1)

{
  short sVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  short asStackY_70050 [6];
  undefined2 auStackY_70044 [229298];
  undefined4 local_cc [16];
  int local_8c;
  uint local_88;
  undefined1 local_84 [16];
  short local_74;
  short local_70;
  short local_6c;
  short local_68;
  short local_64;
  short local_60;
  ushort local_5c;
  short local_58;
  short local_54;
  short asStack_50 [2];
  undefined4 auStack_4c [2];
  undefined2 auStack_44 [30];
  undefined4 local_8;
  
  puVar2 = local_cc;
  for (iVar3 = 0x32; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_54 = 0;
  for (local_58 = 0; local_58 < 5; local_58 = local_58 + 1) {
    puVar2 = (undefined4 *)FUN__text__004a95f0(local_84,local_58);
    iVar3 = (int)local_58;
    *(undefined4 *)(asStack_50 + iVar3 * 7) = *puVar2;
    *(undefined4 *)((int)auStack_4c + iVar3 * 0xe) = puVar2[1];
    *(undefined4 *)((int)auStack_4c + iVar3 * 0xe + 4) = puVar2[2];
    auStack_44[iVar3 * 7] = *(undefined2 *)(puVar2 + 3);
    iVar4 = (int)local_58;
    iVar3 = local_58 * 0x70;
    *(undefined4 *)(&DAT_007a529a + iVar3) = *(undefined4 *)(asStack_50 + iVar4 * 7);
    *(undefined4 *)(&DAT_007a529e + iVar3) = *(undefined4 *)((int)auStack_4c + iVar4 * 0xe);
    *(undefined4 *)(&DAT_007a52a2 + iVar3) = *(undefined4 *)((int)auStack_4c + iVar4 * 0xe + 4);
    *(undefined2 *)(&DAT_007a52a6 + iVar3) = auStack_44[iVar4 * 7];
    if (asStack_50[local_58 * 7] == 2) {
      local_54 = local_54 + 1;
    }
  }
  for (local_58 = 0; sVar1 = DAT_007aab16, local_58 < 5; local_58 = local_58 + 1) {
    *(undefined2 *)(&DAT_007a5304 + local_58 * 0x70) = 0;
  }
  if (local_54 == 0) {
    DAT_007a5296 = 0;
    DAT_007a5298 = 0;
  }
  else {
    local_5c = 0;
    local_60 = 0;
    local_6c = DAT_007aab16;
    DAT_007a5296 = 0;
    DAT_007a5298 = (ushort)(byte)(&DAT_0073bedf)[DAT_007aab16 * 0x100];
    DAT_007a5294 = DAT_007aab16;
    for (local_58 = 0; local_58 < (short)DAT_007a5298; local_58 = local_58 + 1) {
      *(undefined2 *)(&DAT_007a5308 + local_58 * 0x70) =
           *(undefined2 *)(&DAT_0073bee0 + local_58 * 4 + sVar1 * 0x100);
      *(undefined2 *)(&DAT_007a52f8 + local_58 * 0x70) = 0;
      *(undefined2 *)(&DAT_007a5304 + local_58 * 0x70) = 0;
      local_60 = 0;
      local_88 = (uint)(*(ushort *)(&DAT_0073bee2 + sVar1 * 0x100) & 0x7ff);
      if (local_88 != 0) {
        if (local_88 == 1) {
          local_70 = 0;
          local_60 = 0;
          for (local_64 = 0; local_64 < 5; local_64 = local_64 + 1) {
            if (asStack_50[local_64 * 7] == 2) {
              local_70 = *(short *)(&DAT_007a5304 + local_58 * 0x70);
              *(short *)(&DAT_007a5304 + local_58 * 0x70) =
                   *(short *)(&DAT_007a5304 + local_58 * 0x70) + 1;
              *(undefined2 *)(&DAT_007a52fa + local_70 * 2 + local_58 * 0x70) =
                   *(undefined2 *)(&DAT_007aaa12 + local_64 * 0x1c);
              for (local_68 = 0; local_68 < 4; local_68 = local_68 + 1) {
                if (*(short *)(&DAT_007aaa22 + local_68 * 2 + local_64 * 0x1c) != -1) {
                  *(undefined2 *)(&DAT_007a52d0 + local_60 * 2 + local_58 * 0x70) =
                       *(undefined2 *)(&DAT_007aaa22 + local_68 * 2 + local_64 * 0x1c);
                  *(short *)(&DAT_007a52a8 + local_60 * 2 + local_58 * 0x70) = local_64;
                  local_60 = local_60 + 1;
                }
              }
            }
          }
        }
        else if (local_88 == 2) {
          local_74 = 0;
          local_60 = 0;
          for (local_64 = 0; local_64 < 5; local_64 = local_64 + 1) {
            local_5c = 0;
            local_8c = (int)local_64;
            switch((int)local_64) {
            case 0:
              local_5c = *(ushort *)(&DAT_0073bee2 + local_58 * 4 + sVar1 * 0x100) >> 0xb & 1;
              break;
            case 1:
              local_5c = *(ushort *)(&DAT_0073bee2 + local_58 * 4 + sVar1 * 0x100) >> 0xc & 1;
              break;
            case 2:
              local_5c = *(ushort *)(&DAT_0073bee2 + local_58 * 4 + sVar1 * 0x100) >> 0xd & 1;
              break;
            case 3:
              local_5c = *(ushort *)(&DAT_0073bee2 + local_58 * 4 + sVar1 * 0x100) >> 0xe & 1;
              break;
            case 4:
              local_5c = *(ushort *)(&DAT_0073bee2 + local_58 * 4 + sVar1 * 0x100) >> 0xf;
            }
            if (local_5c != 0) {
              local_74 = *(short *)(&DAT_007a5304 + local_58 * 0x70);
              *(short *)(&DAT_007a5304 + local_58 * 0x70) =
                   *(short *)(&DAT_007a5304 + local_58 * 0x70) + 1;
              *(undefined2 *)(&DAT_007a52fa + local_74 * 2 + local_58 * 0x70) =
                   *(undefined2 *)(&DAT_007aaa12 + local_64 * 0x1c);
              for (local_68 = 0; local_68 < 4; local_68 = local_68 + 1) {
                if (*(short *)(&DAT_007aaa22 + local_68 * 2 + local_64 * 0x1c) != -1) {
                  *(undefined2 *)(&DAT_007a52d0 + local_60 * 2 + local_58 * 0x70) =
                       *(undefined2 *)(&DAT_007aaa22 + local_68 * 2 + local_64 * 0x1c);
                  *(short *)(&DAT_007a52a8 + local_60 * 2 + local_58 * 0x70) = local_64;
                  local_60 = local_60 + 1;
                }
              }
            }
          }
        }
      }
      *(short *)(&DAT_007a52f8 + local_58 * 0x70) = local_60;
    }
  }
  local_8 = 0x4a6f6c;
  FUN__text__0056ce80();
  return;
}

