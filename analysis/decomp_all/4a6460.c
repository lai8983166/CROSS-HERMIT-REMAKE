
void __fastcall FUN__text__004a6460(int param_1)

{
  ushort uVar1;
  uint uVar2;
  undefined2 extraout_var;
  int iVar3;
  undefined2 extraout_var_00;
  undefined4 *puVar4;
  undefined4 local_6c [16];
  uint local_2c;
  uint local_28;
  undefined1 local_24;
  short local_20;
  undefined1 local_1c [4];
  uint local_18;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar4 = local_6c;
  for (iVar3 = 0x1a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = CONCAT22(local_c._2_2_,*(undefined2 *)(param_1 + 0x76c6));
  local_20 = 0;
  DAT_007d57dc = (char)DAT_007d57de + -5;
  if (DAT_007d57dc < '\x01') {
    DAT_007d57dc = '\0';
  }
  if (DAT_007d57dc < DAT_007d57db) {
    DAT_007d57db = DAT_007d57dc;
  }
  local_2c = local_2c & 0xffff0000;
  local_8 = param_1;
  while ((local_2c & 0xffff) < 5) {
    uVar1 = (short)DAT_007d57db + (short)local_2c;
    local_28 = CONCAT22(local_28._2_2_,uVar1);
    if ((int)DAT_007d57de <= (int)(uint)uVar1) break;
    FUN__text__004d5ec0(local_1c,(local_2c & 0xffff) * 0x4e + 0x79,0x241,0x44,0x40);
    local_24 = 0xff;
    if (((local_c & 0xffff) == 0) && ((local_10 & 0xffff) != 0)) {
      *(undefined1 *)(local_8 + 0x76c2) = 1;
      local_24 = 0x80;
      if ((local_18 & 2) != 0) {
        if (DAT_007d57c6 == 0) {
          DAT_007d57ca = 0xffff;
        }
        DAT_007d57c6 = (ushort)(DAT_007d57c6 == 0);
        FUN__text__004db2b0(5);
        DAT_007d57c8 = *(undefined2 *)(&DAT_007d57e2 + (local_28 & 0xffff) * 2);
        DAT_007d57cc = (short)local_2c * 0x4e + 0xc0;
        DAT_007d57ce = 0x23b;
        DAT_007d57d0 = (short)local_2c * 0x4e + 0x79;
        DAT_007d57d2 = 0x241;
        DAT_007d57d4 = 0x44;
        DAT_007d57d6 = 0x40;
      }
      if ((local_18 & 1) != 0) {
        DAT_007d598f = '\0';
        DAT_007d598e = '\0';
        DAT_007d5990 = 0xffff;
        DAT_007d5992 = (short)local_28;
        DAT_007d57c2 = *(short *)(&DAT_007d57e2 + (local_28 & 0xffff) * 2);
        DAT_007d5994 = DAT_007d57c2;
        FUN__text__004d48a0(DAT_007d57c2,9,5,0);
        local_c = CONCAT22(local_c._2_2_,6);
      }
    }
    if ((((*(short *)(local_8 + 0x76c6) == 6) && (DAT_007d598f == '\0')) &&
        ((local_28 & 0xffff) == (int)DAT_007d5992)) && (DAT_007d598e == '\0')) {
      local_24 = 0x80;
    }
    uVar2 = local_28 & 0xffff;
    if (DAT_007d57c2 == *(short *)(&DAT_007d57e2 + uVar2 * 2)) {
      FUN__text__004d2700(&DAT_0061b418,1,0x71,(local_2c & 0xffff) * 0x4e + 0x71,0x23a);
      uVar2 = 0;
    }
    local_20 = *(short *)(&DAT_007d57e2 + (local_28 & 0xffff) * 2) + -1;
    FUN__text__004aadb0((local_2c & 0xffff) * 0x4e + 0x75,0x23d,0,(undefined1)local_20,0xff,
                        CONCAT31((int3)(uVar2 >> 8),local_24),0x77);
    FUN__text__004aaf60((local_2c & 0xffff) * 0x4e + 0x79,0x288,0,
                        CONCAT22(extraout_var_00,local_20) & 0xffff00ff,local_24,0x77);
    FUN__text__004aacf0((local_2c & 0xffff) * 0x4e + 0x75,0x23d,
                        (byte)(&DAT_006b2d8a)
                              [*(short *)(&DAT_007e17ee + (local_20 + 1) * 0x4a0) * 0x40] - 1,
                        local_24,0x76);
    local_2c = CONCAT22(local_2c._2_2_,(short)local_2c + 1);
  }
  DAT_007d58ae = DAT_007d58b0 + -5;
  if (DAT_007d58ae < 1) {
    DAT_007d58ae = 0;
  }
  local_2c = local_2c & 0xffff0000;
  while ((local_2c & 0xffff) < 5) {
    uVar1 = DAT_007d58ac + (short)local_2c;
    local_28 = CONCAT22(local_28._2_2_,uVar1);
    if ((int)DAT_007d58b0 <= (int)(uint)uVar1) break;
    FUN__text__004d5ec0(local_1c,(local_2c & 0xffff) * 0x4e + 0x79,0x2a2,0x44,0x40);
    local_24 = 0xff;
    if (((local_c & 0xffff) == 0) && ((local_10 & 0xffff) != 0)) {
      *(undefined1 *)(local_8 + 0x76c2) = 1;
      local_24 = 0x80;
      if ((local_18 & 1) != 0) {
        FUN__text__004db2b0(5);
        DAT_007d598f = '\0';
        DAT_007d598e = '\x01';
        DAT_007d5990 = 0xffff;
        DAT_007d5992 = (short)local_28;
        DAT_007d5994 = *(short *)(&DAT_007d58b4 + (local_28 & 0xffff) * 2);
        local_c = CONCAT22(local_c._2_2_,6);
      }
    }
    if (((*(short *)(local_8 + 0x76c6) == 6) && (DAT_007d598f == '\0')) &&
       (((local_28 & 0xffff) == (int)DAT_007d5992 && (DAT_007d598e == '\x01')))) {
      local_24 = 0x80;
    }
    local_20 = *(short *)(&DAT_007d58b4 + (local_28 & 0xffff) * 2) + -0x65;
    FUN__text__004aadb0((local_2c & 0xffff) * 0x4e + 0x75,0x29e,1,(undefined1)local_20,0xff,local_24
                        ,0x77);
    FUN__text__004aaf60((local_2c & 0xffff) * 0x4e + 0x79,0x2e9,1,
                        CONCAT22(extraout_var,local_20) & 0xffff00ff,local_24,0x77);
    local_2c = CONCAT22(local_2c._2_2_,(short)local_2c + 1);
  }
  *(undefined2 *)(local_8 + 0x76c6) = (undefined2)local_c;
  local_8 = 0x4a6a07;
  FUN__text__0056ce80();
  return;
}

