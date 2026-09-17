
longlong FUN__text__00572860(byte *param_1)

{
  byte *pbVar1;
  uint uVar2;
  longlong lVar3;
  uint local_1c;
  uint local_18;
  int local_10;
  int local_c;
  uint local_8;
  
  while( true ) {
    if (DAT_00764370 < 2) {
      local_18 = *(ushort *)(PTR_DAT_00764164 + (uint)*param_1 * 2) & 8;
    }
    else {
      local_18 = FUN__text__0057bb50(*param_1,8);
    }
    if (local_18 == 0) break;
    param_1 = param_1 + 1;
  }
  uVar2 = (uint)*param_1;
  if ((uVar2 == 0x2d) || (pbVar1 = param_1 + 1, local_8 = uVar2, uVar2 == 0x2b)) {
    local_8 = (uint)param_1[1];
    pbVar1 = param_1 + 2;
  }
  param_1 = pbVar1;
  lVar3 = 0;
  while( true ) {
    local_c = (int)((ulonglong)lVar3 >> 0x20);
    local_10 = (int)lVar3;
    if (DAT_00764370 < 2) {
      local_1c = *(ushort *)(PTR_DAT_00764164 + local_8 * 2) & 4;
    }
    else {
      local_1c = FUN__text__0057bb50(local_8,4);
    }
    if (local_1c == 0) break;
    lVar3 = __allmul(lVar3,10,0);
    lVar3 = lVar3 + (int)(local_8 - 0x30);
    local_8 = (uint)*param_1;
    param_1 = param_1 + 1;
  }
  if (uVar2 == 0x2d) {
    lVar3 = CONCAT44(-(local_c + (uint)(local_10 != 0)),-local_10);
  }
  return lVar3;
}

