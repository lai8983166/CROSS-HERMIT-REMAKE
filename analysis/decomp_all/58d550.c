
uint FUN__text__0058d550(ushort param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined *local_1c;
  ushort local_18 [2];
  uint local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  if ((param_2 == (int *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"_flsbuf.c",0x69,0,"str != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  local_c = param_2;
  local_14 = param_2[4];
  if (((param_2[3] & 0x82U) == 0) || ((param_2[3] & 0x40U) != 0)) {
    param_2[3] = param_2[3] | 0x20;
    uVar3 = 0xffff;
  }
  else {
    if ((param_2[3] & 1U) != 0) {
      param_2[1] = 0;
      if ((param_2[3] & 0x10U) == 0) {
        param_2[3] = param_2[3] | 0x20;
        return 0xffff;
      }
      *param_2 = param_2[2];
      param_2[3] = param_2[3] & 0xfffffffe;
    }
    param_2[3] = param_2[3] | 2;
    param_2[3] = param_2[3] & 0xffffffef;
    param_2[1] = 0;
    local_8 = 0;
    local_10 = 0;
    if (((param_2[3] & 0x10cU) == 0) &&
       (((param_2 != (int *)&DAT_00761ed0 && (param_2 != (int *)&DAT_00761ef0)) ||
        (iVar2 = __isatty(local_14), iVar2 == 0)))) {
      FUN__text__00585b90(local_c);
    }
    local_18[0] = param_1;
    if ((local_c[3] & 0x108U) == 0) {
      local_8 = 2;
      local_10 = FUN__text__0057c550(local_14,local_18,2);
    }
    else {
      if ((*local_c - local_c[2] < 0) &&
         (iVar2 = FUN__text__00573780(2,"_flsbuf.c",0xa0,0,
                                      "(\"inconsistent IOB fields\", stream->_ptr - stream->_base >= 0)"
                                     ), iVar2 == 1)) {
        pcVar1 = (code *)swi(3);
        uVar3 = (*pcVar1)();
        return uVar3;
      }
      local_8 = *local_c - local_c[2];
      *local_c = local_c[2] + 2;
      local_c[1] = local_c[6] + -2;
      if (local_8 < 1) {
        if (local_14 == 0xffffffff) {
          local_1c = &DAT_007644d0;
        }
        else {
          local_1c = (undefined *)((&DAT_0080a800)[(int)local_14 >> 5] + (local_14 & 0x1f) * 0x24);
        }
        if ((local_1c[4] & 0x20) != 0) {
          FUN__text__00585a40(local_14,0,2);
        }
      }
      else {
        local_10 = FUN__text__0057c550(local_14,local_c[2],local_8);
      }
      *(ushort *)local_c[2] = param_1;
    }
    if (local_10 == local_8) {
      uVar3 = (uint)param_1;
    }
    else {
      local_c[3] = local_c[3] | 0x20;
      uVar3 = 0xffff;
    }
  }
  return uVar3;
}

