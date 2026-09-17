
void FUN__text__00441630(uint param_1,undefined4 *param_2,short param_3,short param_4,
                        undefined2 param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  int local_34;
  char local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  int local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (int)param_3 - 200;
  local_1c = (int)param_4 - 0x55;
  if ((((int)param_1 < 0) || (0x31 < param_1)) &&
     (iVar2 = FUN__text__00424f80("(0<=setno) && (setno<(sizeof(MesStrWork)/sizeof(SysMessageBoxWork)))"
                                  ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\MesBox.cpp",
                                  DAT_005ffc70 + 0x10,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = &DAT_005ffa90 + param_1 * 8;
  local_10 = 0;
  local_30 = *local_c;
  if (local_30 == '\0') {
    local_20 = local_18 + (int)DAT_005ffc20;
    local_24 = local_1c + (int)DAT_005ffc22;
    local_28 = (int)DAT_005ffc24;
    local_2c = (int)DAT_005ffc26;
    iVar2 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                *(undefined4 *)(DAT_007a49fc + 0x1970),local_20,local_24,local_28,
                                local_2c);
    if (iVar2 != 0) {
      local_10 = 1;
    }
  }
  else if (local_30 == '\x01') {
    local_20 = local_18 + (int)DAT_005ffc28;
    local_24 = local_1c + (int)DAT_005ffc2a;
    local_28 = (int)DAT_005ffc2c;
    local_2c = (int)DAT_005ffc2e;
    iVar2 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                *(undefined4 *)(DAT_007a49fc + 0x1970),local_20,local_24,local_28,
                                local_2c);
    if (iVar2 != 0) {
      local_10 = 2;
    }
    local_20 = local_18 + (int)DAT_005ffc30;
    local_24 = local_1c + (int)DAT_005ffc32;
    local_28 = (int)DAT_005ffc34;
    local_2c = (int)DAT_005ffc36;
    iVar2 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                *(undefined4 *)(DAT_007a49fc + 0x1970),local_20,local_24,local_28,
                                local_2c);
    if (iVar2 != 0) {
      local_10 = 3;
    }
  }
  *param_2 = 0xffffffff;
  if ((local_10 != 0) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
    local_34 = local_10;
    if (local_10 == 0) {
      *param_2 = 0;
    }
    else if (local_10 == 1) {
      *param_2 = 1;
    }
    else if (local_10 == 2) {
      *param_2 = 0;
    }
    FUN__text__004db2b0(5);
  }
  local_14 = -1;
  if (((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) && (local_10 != 0)) {
    local_14 = local_10 + -1;
  }
  FUN__text__004418f0(local_c,local_14,local_18 & 0xffff,local_1c & 0xffff,param_5);
  local_8 = 0x4418db;
  FUN__text__0056ce80();
  return;
}

