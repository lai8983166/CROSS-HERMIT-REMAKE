
uint FUN_005756c0(uint param_1,int *param_2)

{
  code *pcVar1;
  int *piVar2;
  int iVar3;
  uint uVar4;
  undefined *local_18;
  int local_10;
  int local_8;
  
  if ((param_2 == (int *)0x0) &&
     (iVar3 = FUN_00573780(2,"_flsbuf.c",0x69,0,"str != NULL"), iVar3 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar4 = (*pcVar1)();
    return uVar4;
  }
  piVar2 = param_2;
  uVar4 = param_2[4];
  if (((param_2[3] & 0x82U) == 0) || ((param_2[3] & 0x40U) != 0)) {
    param_2[3] = param_2[3] | 0x20;
    param_1 = 0xffffffff;
  }
  else {
    if ((param_2[3] & 1U) != 0) {
      param_2[1] = 0;
      if ((param_2[3] & 0x10U) == 0) {
        param_2[3] = param_2[3] | 0x20;
        return 0xffffffff;
      }
      *param_2 = param_2[2];
      param_2[3] = param_2[3] & 0xfffffffe;
    }
    param_2[3] = param_2[3] | 2;
    param_2[3] = param_2[3] & 0xffffffef;
    param_2[1] = 0;
    local_10 = 0;
    if (((param_2[3] & 0x10cU) == 0) &&
       (((param_2 != (int *)&DAT_00761ed0 && (param_2 != (int *)&DAT_00761ef0)) ||
        (iVar3 = __isatty(uVar4), iVar3 == 0)))) {
      FUN_00585b90(piVar2);
    }
    if ((piVar2[3] & 0x108U) == 0) {
      local_8 = 1;
      local_10 = FUN_0057c550(uVar4,&param_1,1);
    }
    else {
      if ((*piVar2 - piVar2[2] < 0) &&
         (iVar3 = FUN_00573780(2,"_flsbuf.c",0xa0,0,
                               "(\"inconsistent IOB fields\", stream->_ptr - stream->_base >= 0)"),
         iVar3 == 1)) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      local_8 = *piVar2 - piVar2[2];
      *piVar2 = piVar2[2] + 1;
      piVar2[1] = piVar2[6] + -1;
      if (local_8 < 1) {
        if (uVar4 == 0xffffffff) {
          local_18 = &DAT_007644d0;
        }
        else {
          local_18 = (undefined *)((&DAT_0080a800)[(int)uVar4 >> 5] + (uVar4 & 0x1f) * 0x24);
        }
        if ((local_18[4] & 0x20) != 0) {
          FUN_00585a40(uVar4,0,2);
        }
      }
      else {
        local_10 = FUN_0057c550(uVar4,piVar2[2],local_8);
      }
      *(undefined1 *)piVar2[2] = (undefined1)param_1;
    }
    if (local_10 == local_8) {
      param_1 = param_1 & 0xff;
    }
    else {
      piVar2[3] = piVar2[3] | 0x20;
      param_1 = 0xffffffff;
    }
  }
  return param_1;
}

