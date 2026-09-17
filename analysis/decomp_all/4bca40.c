
void FUN__text__004bca40(void)

{
  short sVar1;
  short sVar2;
  short sVar3;
  int extraout_ECX;
  int iVar4;
  undefined4 *puVar5;
  short asStack_b1a30 [328140];
  short asStack_11698 [32232];
  undefined4 local_1ac8 [16];
  short local_1a88;
  short local_1a84;
  short local_1a80;
  short local_1a7c;
  short local_1a78;
  short local_1a74;
  short local_1a70;
  short local_1a6c;
  short local_1a68;
  short local_1a64;
  short local_1a60;
  short local_1a5c;
  short asStack_1a5a [11];
  short asStack_1a44 [10];
  short asStack_1a30 [90];
  short asStack_197c [10];
  short asStack_1968 [3240];
  short local_18;
  undefined4 local_14;
  
  FUN__text__0056e230();
  puVar5 = local_1ac8;
  for (iVar4 = 0x6b1; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_14 = CONCAT22((short)((uint)extraout_ECX >> 0x10),DAT_007a5294);
  local_18 = DAT_007f450c + -1;
  if ((short)(DAT_007f450c + -1) < 0) {
    local_18 = 0;
  }
  for (sVar1 = 0; sVar1 < 9; sVar1 = sVar1 + 1) {
    asStack_1a44[sVar1] = 0;
    asStack_197c[sVar1] = 0;
    asStack_1a5a[sVar1 + 1] = 0;
  }
  for (sVar1 = 0; sVar1 < 0x168; sVar1 = sVar1 + 1) {
    local_1a5c = *(short *)(&DAT_006d5120 + (sVar1 + 1) * 0x38);
    if (0 < local_1a5c) {
      local_1a64 = asStack_197c[local_1a5c];
      asStack_197c[local_1a5c] = asStack_197c[local_1a5c] + 1;
      asStack_1968[local_1a5c * 0x168 + (int)local_1a64] = sVar1;
    }
  }
  for (sVar1 = 0; sVar1 < 7; sVar1 = sVar1 + 1) {
    local_1a68 = local_18 * 7 + sVar1;
    local_1a6c = *(short *)(&DAT_0073bf1a + local_1a68 * 2 + (short)local_14 * 0x100);
    asStack_1a5a[8 - sVar1] = *(short *)(&DAT_0073bf1a + local_1a68 * 2 + (short)local_14 * 0x100);
  }
  for (sVar1 = 0; sVar1 < 8; sVar1 = sVar1 + 1) {
    local_1a60 = *(short *)(&DAT_0073bf60 + sVar1 * 2 + (short)local_14 * 0x100);
    if ((0 < local_1a60) && ((*(ushort *)(&DAT_007aacaa + local_1a60 * 2) & 1) != 1)) {
      local_1a5c = *(short *)(&DAT_006d5120 + local_1a60 * 0x38);
      if (0 < local_1a5c) {
        local_1a64 = asStack_1a44[local_1a5c];
        if (local_1a64 < 10) {
          asStack_1a30[local_1a5c * 10 + (int)local_1a64] = local_1a60;
          asStack_1a44[local_1a5c] = asStack_1a44[local_1a5c] + 1;
          *(ushort *)(&DAT_007aacaa + local_1a60 * 2) =
               *(ushort *)(&DAT_007aacaa + local_1a60 * 2) | 1;
          *(ushort *)(&DAT_007aacaa + local_1a60 * 2) =
               *(ushort *)(&DAT_007aacaa + local_1a60 * 2) & 0xf0ff | 0x100;
        }
      }
    }
  }
  for (sVar1 = 0; sVar1 < 0x10; sVar1 = sVar1 + 1) {
    if ((&DAT_007f44be)[sVar1] != '\0') {
      local_1a60 = *(short *)(&DAT_0073bf70 + sVar1 * 6 + (short)local_14 * 0x100);
      if (local_1a60 < 1) {
        local_1a70 = *(short *)(&DAT_0073bf72 + sVar1 * 6 + (short)local_14 * 0x100);
        local_1a74 = *(short *)(&DAT_0073bf74 + sVar1 * 6 + (short)local_14 * 0x100);
        asStack_1a5a[local_1a70 + 1] =
             asStack_1a5a[local_1a70 + 1] +
             *(short *)(&DAT_0073bf74 + sVar1 * 6 + (short)local_14 * 0x100);
      }
      else if ((*(ushort *)(&DAT_007aacaa + local_1a60 * 2) & 1) == 1) {
        local_1a5c = *(short *)(&DAT_006d5120 + local_1a60 * 0x38);
        asStack_1a5a[local_1a5c] = asStack_1a5a[local_1a5c] + 2;
      }
      else {
        local_1a5c = *(short *)(&DAT_006d5120 + local_1a60 * 0x38);
        if (0 < local_1a5c) {
          local_1a64 = asStack_1a44[local_1a5c];
          if (local_1a64 < 10) {
            asStack_1a30[local_1a5c * 10 + (int)local_1a64] = local_1a60;
            asStack_1a44[local_1a5c] = asStack_1a44[local_1a5c] + 1;
            *(ushort *)(&DAT_007aacaa + local_1a60 * 2) =
                 *(ushort *)(&DAT_007aacaa + local_1a60 * 2) | 1;
            *(ushort *)(&DAT_007aacaa + local_1a60 * 2) =
                 *(ushort *)(&DAT_007aacaa + local_1a60 * 2) & 0xf0ff | 0x100;
          }
        }
      }
    }
  }
  local_14 = 0x4bcf69;
  FUN__text__004d1c60();
  for (sVar1 = 7; 0 < sVar1; sVar1 = sVar1 + -1) {
    for (sVar3 = 0; sVar3 < asStack_1a5a[sVar1 + 1]; sVar3 = sVar3 + 1) {
      local_1a78 = asStack_197c[sVar1];
      if (asStack_197c[sVar1] == 0) {
        asStack_1a5a[sVar1] = asStack_1a5a[sVar1] + 2;
      }
      else {
        local_14 = 0x4bcffe;
        sVar2 = FUN__text__004d1cb0();
        local_1a7c = sVar2 % local_1a78;
        local_1a80 = asStack_1968[sVar1 * 0x168 + (int)(sVar2 % local_1a78)];
        local_1a84 = *(short *)(&DAT_006d5120 + (local_1a80 + 1) * 0x38);
        if ((*(ushort *)(&DAT_007aacac + local_1a80 * 2) & 1) == 0) {
          if (0 < local_1a84) {
            local_1a88 = asStack_1a44[local_1a84];
            if (local_1a88 < 10) {
              asStack_1a44[local_1a84] = asStack_1a44[local_1a84] + 1;
              asStack_1a30[local_1a84 * 10 + (int)local_1a88] = local_1a80 + 1;
              *(ushort *)(&DAT_007aacac + local_1a80 * 2) =
                   *(ushort *)(&DAT_007aacac + local_1a80 * 2) | 1;
              *(ushort *)(&DAT_007aacac + local_1a80 * 2) =
                   *(ushort *)(&DAT_007aacac + local_1a80 * 2) & 0xf0ff | 0x100;
            }
          }
        }
        else {
          asStack_1a5a[sVar1] = asStack_1a5a[sVar1] + 2;
        }
      }
    }
  }
  for (sVar1 = 7; 0 < sVar1; sVar1 = sVar1 + -1) {
    for (sVar3 = 0; sVar3 < asStack_1a44[sVar1]; sVar3 = sVar3 + 1) {
      *(short *)(extraout_ECX + 0x140 + (7 - sVar1) * 0x14 + sVar3 * 2) =
           asStack_1a30[sVar1 * 10 + (int)sVar3];
    }
  }
  FUN__text__0056ce80();
  return;
}

