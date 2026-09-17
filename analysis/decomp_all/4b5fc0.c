
void FUN__text__004b5fc0(void)

{
  byte bVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined2 uVar3;
  undefined4 *puVar4;
  undefined4 local_70 [16];
  char local_30;
  byte local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  undefined4 local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar4 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  DAT_007d6a30 = '\0';
  FUN__text__004d2700(&DAT_0061bb60,1,0x4f,8,0x1b4);
  FUN__text__004d2700(&DAT_0061bae0,1,0x4f,0,2);
  FUN__text__004d2700(&DAT_0061bae0,1,0x4f,0,0x1a5);
  if (DAT_007d6a31 == '\0') {
    FUN__text__004b28f0();
  }
  else {
    FUN__text__004b4000(0);
  }
  FUN__text__004d69e0();
  local_1c = (uint)local_1c._2_2_ << 0x10;
  while ((local_1c & 0xffff) < 7) {
    if ((((local_1c & 0xffff) != 5) &&
        (FUN__text__004d5c40(local_18,(local_1c & 0xffff) + 0x19), bVar1 = DAT_007d6a32,
        (local_c & 0xffff) != 0)) && ((local_14 & 1) != 0)) {
      DAT_007d6a33 = DAT_007d6a32;
      DAT_007d6a32 = (byte)local_1c;
      if ((uint)bVar1 != (local_1c & 0xff)) {
        FUN__text__004b5a00();
        local_20 = local_1c & 0xffff;
        switch(local_20) {
        case 0:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0a0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
          break;
        case 1:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0b0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
          break;
        case 2:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0c0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
          break;
        case 3:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0d0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
          break;
        case 4:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0e0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
          break;
        case 6:
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_0061c0f0,0x3e,8,0x2ce,6);
        }
        if (DAT_007d6a32 == 6) {
          DAT_007d6a32 = DAT_007d6a33;
          DAT_007a4e60 = 2;
        }
      }
    }
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  *(undefined1 *)(local_8 + 0xc88) = 0;
  local_24 = (uint)DAT_007d6a32;
  switch(local_24) {
  case 0:
    FUN__text__004ae370();
    break;
  case 1:
    FUN__text__004afb70();
    break;
  case 2:
    FUN__text__004b12a0();
    break;
  case 3:
    FUN__text__004abb60();
    break;
  case 4:
    FUN__text__004b3bb0();
    break;
  case 6:
  }
  if (*(char *)(local_8 + 0xc88) != '\0') {
    local_1c = CONCAT22(local_1c._2_2_,0xffff);
    iVar2 = FUN__text__004128f0(200,1);
    if (iVar2 != 0) {
      FUN__text__004b5a00();
      if (DAT_007d6a32 == 0) {
        DAT_007d6a32 = 4;
      }
      else {
        DAT_007d6a32 = DAT_007d6a32 - 1;
      }
      local_1c = CONCAT22(local_1c._2_2_,(ushort)DAT_007d6a32);
      FUN__text__004db2b0(5);
    }
    iVar2 = FUN__text__004128f0(0xd0,1);
    if (iVar2 != 0) {
      FUN__text__004b5a00();
      if (DAT_007d6a32 == 4) {
        DAT_007d6a32 = 0;
      }
      else {
        DAT_007d6a32 = DAT_007d6a32 + 1;
      }
      local_1c = CONCAT22(local_1c._2_2_,(ushort)DAT_007d6a32);
      FUN__text__004db2b0(5);
    }
    local_28 = local_1c & 0xffff;
    switch(local_28) {
    case 0:
      FUN__text__004d68b0(&DAT_0061c0a0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
      break;
    case 1:
      FUN__text__004d68b0(&DAT_0061c0b0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
      break;
    case 2:
      FUN__text__004d68b0(&DAT_0061c0c0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
      break;
    case 3:
      FUN__text__004d68b0(&DAT_0061c0d0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
      break;
    case 4:
      FUN__text__004d68b0(&DAT_0061c0e0,0x3e,8,(local_1c & 0xffff) * 0x2f + 0x1b4,6);
    }
    local_8 = 0;
  }
  uVar3 = (undefined2)((uint)local_8 >> 0x10);
  local_2c = DAT_007d6a32;
  if (DAT_007d6a32 < 3) {
    FUN__text__004b5050();
    FUN__text__004b52f0();
    uVar3 = extraout_var;
  }
  if (DAT_007d6a32 != 5) {
    if (DAT_007d6a32 == 6) {
      uVar3 = 0;
    }
    else {
      FUN__text__004d2790(&DAT_0061bb70,1,0x48,8,(uint)DAT_007d6a32 * 0x2f + 0x1b4,0,
                          (DAT_007d6a32 + 6) * 0x2c);
      uVar3 = 0;
    }
  }
  local_30 = DAT_007d6a30;
  if (DAT_007d6a30 == '\0') {
    FUN__text__004d2700(&DAT_0061bd20,1,0x33,*(undefined2 *)(DAT_007a49fc + 0x196c),
                        CONCAT22(uVar3,*(undefined2 *)(DAT_007a49fc + 0x1970)));
  }
  else if (DAT_007d6a30 == '\x01') {
    FUN__text__004d2700(&DAT_0061bd30,1,0x33,*(short *)(DAT_007a49fc + 0x196c) + -0x12,
                        *(short *)(DAT_007a49fc + 0x1970) + -0x12);
  }
  else if (DAT_007d6a30 == '\x02') {
    FUN__text__004d2700(&DAT_0061bd40,1,0x33,*(short *)(DAT_007a49fc + 0x196c) + -0x12,
                        *(short *)(DAT_007a49fc + 0x1970) + -0x12);
  }
  local_8 = 0x4b6639;
  FUN__text__0056ce80();
  return;
}

