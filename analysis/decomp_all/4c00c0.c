
void __fastcall FUN__text__004c00c0(int param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  int local_2c;
  short local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_6c;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 < 5; local_10 = local_10 + 1) {
    local_20 = *(short *)(&DAT_007a529a + local_10 * 0x70);
    local_2c = (int)local_20;
    if (local_2c == 2) {
      local_1c = 1;
      *(undefined2 *)(local_8 + 0x142e) = 0;
    }
    else if (local_2c == 4) {
      local_1c = 0;
    }
    for (local_c = 0; local_c < 4; local_c = local_c + 1) {
      local_14 = *(short *)(&DAT_007aaae0 + local_10 * 8 + local_c * 2);
      if (local_14 < 0) {
        FUN__text__004d2620(local_c * 0xc6 + 0xe7,local_10 * 0x8a + 0x27,0xc6,0x86,0x52,0xa0010101,1
                           );
      }
      else {
        local_18 = *(short *)(&DAT_007a5210 + local_14 * 2);
        if (local_1c == 0) {
          FUN__text__004c0400(local_18,CONCAT22(local_c >> 0xf,local_10));
        }
        else {
          FUN__text__004c0c10(CONCAT22(local_14 >> 0xf,local_18));
        }
        for (local_24 = 0; local_24 < 7; local_24 = local_24 + 1) {
          sVar1 = (ushort)(byte)(&DAT_007e17f4)[local_24 * 8 + local_18 * 0x4a0] -
                  *(short *)(local_8 + local_18 * 0x44 + 0x5c + local_24 * 2);
          if (DAT_007e118e < sVar1) {
            DAT_007e118e = sVar1;
          }
        }
        if ((DAT_007e1184 < *(int *)(&DAT_007cf36c + local_18 * 0x124)) && (local_18 < 0xd)) {
          DAT_007e1184 = *(int *)(&DAT_007cf36c + local_18 * 0x124);
          DAT_007e1180 = local_18;
          DAT_007e1182 = *(undefined2 *)(&DAT_007cf46c + local_18 * 0x124);
        }
        if (DAT_007e1188 < *(int *)(&DAT_007cf36c + local_18 * 0x124)) {
          DAT_007e1188 = *(int *)(&DAT_007cf36c + local_18 * 0x124);
        }
        local_28 = (ushort)(byte)(&DAT_007e1838)[local_18 * 0x4a0] -
                   *(short *)(local_8 + 0x5a + local_18 * 0x44);
        if (DAT_007e118c < local_28) {
          DAT_007e118c = local_28;
        }
      }
    }
  }
  local_8 = 0x4c0346;
  FUN__text__0056ce80();
  return;
}

