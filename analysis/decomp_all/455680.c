
void __thiscall FUN__text__00455680(int param_1,undefined2 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [16];
  int local_2c;
  int local_28;
  undefined4 local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = 0x12;
  local_c = *(int *)(param_1 + 0x60) + 0x20ec;
  local_14 = 0x60;
  local_18 = 0x20;
  local_24 = 0x20;
  local_20 = 1;
  local_8 = param_1;
  FUN__text__0040ec50(0x60,0x20,param_2,0xffffffff,0,"ScriptTimer");
  for (local_10 = 0; local_10 != 0x10; local_10 = local_10 + 1) {
    if (*(char *)(local_c + local_10 * 8) == -1) {
      local_28 = (int)local_18 + (int)local_1c * (int)local_20;
      local_20 = local_20 + 1;
      FUN__text__0040ed20(DAT_007a49fc + 0x1058,(int)local_14,local_28,param_2,0xffffffff,0,
                          "(%02d):",local_10);
    }
    else {
      local_2c = (int)local_18 + (int)local_1c * (int)local_20;
      local_20 = local_20 + 1;
      FUN__text__0040ed20(DAT_007a49fc + 0x1058,(int)local_14,local_2c,param_2,0xffffffff,0,
                          "(%02d):(%2d,%2d):%8d(V)",local_10,
                          (int)*(char *)(local_c + 1 + local_10 * 8),
                          (int)*(short *)(local_c + 2 + local_10 * 8),
                          *(undefined4 *)(local_c + 4 + local_10 * 8));
    }
  }
  local_8 = 0x45580a;
  FUN__text__0056ce80();
  return;
}

