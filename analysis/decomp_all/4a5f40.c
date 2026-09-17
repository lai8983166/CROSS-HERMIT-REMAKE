
void __fastcall FUN__text__004a5f40(undefined4 param_1)

{
  char cVar1;
  short sVar2;
  uint uVar3;
  int iVar4;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar5;
  undefined4 local_6c [16];
  undefined2 local_2c;
  short local_28;
  undefined2 local_24;
  undefined2 local_20;
  undefined2 local_1c;
  undefined2 local_18;
  short local_14;
  uint local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  sVar2 = DAT_007a55f8;
  puVar5 = local_6c;
  for (iVar4 = 0x1a; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_14 = DAT_007a55f8;
  DAT_007a55f8 = 0;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 5) {
    if (sVar2 != 0) {
      (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 1;
      (&DAT_007aaa16)[(local_c & 0xffff) * 0x1c] = 0xff;
      *(undefined2 *)(&DAT_007aaa18 + (local_c & 0xffff) * 0x1c) = 0xffff;
      *(undefined2 *)(&DAT_007aaa1a + (local_c & 0xffff) * 0x1c) = 0xffff;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  DAT_007d57db = 0;
  DAT_007d57da = 0;
  DAT_007d57de = 0;
  DAT_007d57e0 = DAT_007a5260;
  local_c = (uint)local_c._2_2_ << 0x10;
  local_8 = param_1;
  while ((int)(local_c & 0xffff) < (int)DAT_007a5260) {
    FUN__text__004ab250(*(undefined2 *)(&DAT_007a5210 + (local_c & 0xffff) * 2));
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  DAT_007d58ac = 0;
  DAT_007d58aa = 0;
  DAT_007d58b0 = 0;
  DAT_007d58b2 = DAT_007a528a;
  local_c = local_c & 0xffff0000;
  while (iVar4 = (int)DAT_007a528a, (int)(local_c & 0xffff) < iVar4) {
    FUN__text__004ab3e0(*(undefined2 *)(&DAT_007a5262 + (local_c & 0xffff) * 2));
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_18 = 0;
  local_1c = 0;
  local_20 = 0;
  local_28 = 1;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 5) {
    if (local_14 != 0) {
      iVar4 = (local_c & 0xffff) * 0x1c;
      (&DAT_007aaa15)[iVar4] = 1;
    }
    local_24 = *(undefined2 *)(&DAT_007aaa12 + (local_c & 0xffff) * 0x1c);
    sVar2 = FUN__text__004d46e0(CONCAT22((short)((uint)iVar4 >> 0x10),local_24));
    if (sVar2 == 0) {
      *(undefined2 *)(&DAT_007aaaae + (local_c & 0xffff) * 2) = 0xffff;
      *(undefined2 *)(&DAT_007aaaa4 + (local_c & 0xffff) * 2) = 0xffff;
      (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 1;
      uVar3 = (local_c & 0xffff) * 0x1c;
      *(undefined2 *)(&DAT_007aaa12 + uVar3) = 0xffff;
    }
    else {
      FUN__text__004ab470(CONCAT22(extraout_var_00,local_24));
      uVar3 = 0;
      if (local_28 != 0) {
        uVar3 = FUN__text__004a8b50(CONCAT22(extraout_var,(short)local_c));
        local_28 = 0;
      }
      if (local_14 != 0) {
        uVar3 = (uint)DAT_007a55fa;
        if (uVar3 != 0) {
          (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 0;
        }
        (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 0;
      }
    }
    iVar4 = CONCAT22((short)(uVar3 >> 0x10),(short)local_c + 1);
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 5) {
    (&DAT_007aaa20)[(local_c & 0xffff) * 0x1c] = 0;
    local_10 = local_10 & 0xffff0000;
    while ((local_10 & 0xffff) < 4) {
      iVar4 = (local_c & 0xffff) * 0x1c;
      local_2c = *(undefined2 *)(&DAT_007aaa22 + (local_10 & 0xffff) * 2 + iVar4);
      sVar2 = FUN__text__004d46e0(CONCAT22((short)((uint)iVar4 >> 0x10),local_2c));
      if (sVar2 == 0) {
        *(undefined2 *)(&DAT_007aaae0 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff;
        *(undefined2 *)(&DAT_007aaab8 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff;
        *(undefined2 *)(&DAT_007aaa22 + (local_10 & 0xffff) * 2 + (local_c & 0xffff) * 0x1c) =
             0xffff;
      }
      else if (*(short *)(&DAT_007aaa12 + (local_c & 0xffff) * 0x1c) == -1) {
        *(undefined2 *)(&DAT_007aaae0 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff;
        *(undefined2 *)(&DAT_007aaab8 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff;
        *(undefined2 *)(&DAT_007aaa22 + (local_10 & 0xffff) * 2 + (local_c & 0xffff) * 0x1c) =
             0xffff;
      }
      else {
        cVar1 = FUN__text__004ab2e0(CONCAT22(sVar2 >> 0xf,local_2c));
        if (cVar1 == '\x01') {
          *(short *)(&DAT_007aaa22 + (local_10 & 0xffff) * 2 + (local_c & 0xffff) * 0x1c) =
               (short)(char)local_2c;
          (&DAT_007aaa20)[(local_c & 0xffff) * 0x1c] =
               (&DAT_007aaa20)[(local_c & 0xffff) * 0x1c] + '\x01';
        }
        else {
          *(undefined2 *)(&DAT_007aaae0 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff
          ;
          *(undefined2 *)(&DAT_007aaab8 + (local_c & 0xffff) * 8 + (local_10 & 0xffff) * 2) = 0xffff
          ;
          *(undefined2 *)(&DAT_007aaa22 + (local_10 & 0xffff) * 2 + (local_c & 0xffff) * 0x1c) =
               0xffff;
        }
      }
      local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4a644e;
  FUN__text__0056ce80();
  return;
}

