
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__00572e90(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  size_t sVar3;
  char *pcVar4;
  undefined4 uVar5;
  uint local_ac [2];
  undefined4 local_a4;
  char local_a0 [132];
  undefined4 local_1c;
  undefined1 local_18 [8];
  undefined *local_10;
  int local_c;
  undefined4 local_8;
  
  iVar1 = FUN__text__00573130(param_2,local_a0,local_ac,&local_a4,param_1);
  if (iVar1 == 0) {
    uVar2 = 0;
  }
  else {
    uVar5 = 0x132;
    pcVar4 = "setlocal.c";
    uVar2 = 2;
    sVar3 = _strlen(local_a0);
    local_c = __malloc_dbg(sVar3 + 1,uVar2,pcVar4,uVar5);
    if (local_c == 0) {
      uVar2 = 0;
    }
    else {
      local_10 = (undefined *)(&DAT_00761b2c)[param_1 * 3];
      local_8 = *(undefined4 *)(&DAT_0080a624 + param_1 * 4);
      FUN__text__0056d4d0(local_18,&DAT_0080a644 + param_1 * 6,6);
      local_1c = DAT_0080a63c;
      uVar2 = FUN__text__0056cd90(local_c,local_a0);
      (&DAT_00761b2c)[param_1 * 3] = uVar2;
      *(uint *)(&DAT_0080a624 + param_1 * 4) = local_ac[0] & 0xffff;
      FUN__text__0056d4d0(&DAT_0080a644 + param_1 * 6,local_ac,6);
      if (param_1 == 2) {
        DAT_0080a63c = local_a4;
      }
      if (param_1 == 1) {
        _DAT_0080a640 = local_a4;
      }
      iVar1 = (**(code **)(&DAT_00761b30 + param_1 * 0xc))();
      if (iVar1 == 0) {
        if (local_10 != &DAT_00761a18) {
          __free_dbg(local_10,2);
        }
        uVar2 = (&DAT_00761b2c)[param_1 * 3];
      }
      else {
        (&DAT_00761b2c)[param_1 * 3] = local_10;
        __free_dbg(local_c,2);
        *(undefined4 *)(&DAT_0080a624 + param_1 * 4) = local_8;
        DAT_0080a63c = local_1c;
        uVar2 = 0;
      }
    }
  }
  return uVar2;
}

