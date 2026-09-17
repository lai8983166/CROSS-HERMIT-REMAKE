
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void tick_0x426820(undefined4 param_1,int param_2,uint param_3,int param_4,int param_5,
                  undefined4 param_6,undefined4 param_7,undefined2 param_8)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  uint uVar2;
  undefined2 uVar3;
  undefined2 extraout_var_03;
  undefined4 *puVar4;
  undefined8 uVar5;
  undefined4 auStack_464 [16];
  int iStack_424;
  undefined1 auStack_420 [968];
  undefined *puStack_58;
  int iStack_20;
  int iStack_1c;
  int iStack_18;
  int iStack_14;
  uint uStack_10;
  int iStack_c;
  int iStack_8;
  
  puVar4 = auStack_464;
  for (iVar1 = 0x118; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar1 = func_0x00425c70();
  if (iVar1 == 0) {
    func_0x004077c0(param_1);
    FUN_0056cd90(auStack_420,iStack_8 + 0x63c);
    (*API_KERNEL32_DLL_GetTickCount)();
    uVar5 = __chkesp();
    uVar2 = (uint)((ulonglong)uVar5 >> 0x20);
    iStack_424 = (int)uVar5;
    if (300 < iStack_424 - _DAT_0079fc64) {
      uVar2 = DAT_0079fc6c ^ 1;
      _DAT_0079fc64 = iStack_424;
      DAT_0079fc6c = uVar2;
    }
    uVar3 = (undefined2)(uVar2 >> 0x10);
    if (DAT_0079fc6c != 0) {
      FUN_0056cda0(auStack_420,&DAT_00594bd8);
      uVar3 = extraout_var_03;
    }
    func_0x00409770(CONCAT22((short)((uint)auStack_420 >> 0x10),(undefined2)param_2),
                    param_3 & 0xffff,CONCAT22(uVar3,param_8),0xffffffff,auStack_420);
  }
  else {
    if (param_5 == 0) {
      iStack_14 = param_4;
    }
    else {
      iStack_14 = param_5;
    }
    (*API_KERNEL32_DLL_lstrlenA)(iStack_8 + 0x63c);
    iStack_1c = __chkesp();
    func_0x004077c0(param_1);
    func_0x00409770(CONCAT22((short)((uint)(iStack_8 + 0x63c) >> 0x10),(undefined2)param_2),
                    CONCAT22(extraout_var,(undefined2)param_3),CONCAT22(extraout_var_01,param_8),
                    0xffffffff,iStack_8 + 0x63c);
    iStack_18 = func_0x00426040();
    iStack_c = param_2 + iStack_1c * (param_4 / 2);
    uStack_10 = param_3;
    func_0x004077c0(param_1);
    func_0x00409770(CONCAT22((short)((uint)(iStack_8 + 0x528) >> 0x10),(undefined2)iStack_c),
                    CONCAT22(extraout_var_02,(undefined2)uStack_10),
                    CONCAT22(extraout_var_00,param_8),0xffffd080,iStack_8 + 0x528);
    iVar1 = iStack_18 * (param_4 / 2);
    iStack_c = param_2 + iVar1 + iStack_1c * (param_4 / 2);
    uStack_10 = param_3;
    func_0x00410310(iStack_c,param_3,2,iStack_14,CONCAT22((short)((uint)iVar1 >> 0x10),param_8),
                    0xffffffff,0);
    for (iStack_20 = 0; iStack_20 < DAT_0079fc70; iStack_20 = iStack_20 + 1) {
      iStack_c = 0x32;
      uStack_10 = iStack_20 * 0x18;
      func_0x00409770(CONCAT22((short)((uint)(&DAT_0079aa44 + iStack_20 * 200) >> 0x10),0x32),
                      uStack_10,CONCAT22((short)((uint)iStack_20 >> 0x10),param_8),0xffffd080,
                      &DAT_0079aa44 + iStack_20 * 200);
    }
  }
  puStack_58 = &UNK_00426a70;
  __chkesp();
  return;
}

