
void FUN_00422090(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int *local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1[8] == 0) {
    FUN_0042b2d0(&DAT_005949f8,param_1);
    iVar2 = FUN_00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                         DAT_005ff60c + 0x22,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    FUN_0042b2d0(&DAT_00594a24,param_1,param_1[8]);
    (*DAT_00592260)(param_1[8],0);
    local_c = __chkesp();
    if ((local_c == 0) &&
       (iVar2 = FUN_00424f80("hret!=0","E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                             DAT_005ff60c + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = 0;
    while( true ) {
      (*DAT_00592264)(10);
      __chkesp();
      (*API_KERNEL32_DLL_GetExitCodeThread)(param_1[8],&local_10);
      local_c = __chkesp();
      if ((local_c == 0) &&
         (iVar2 = FUN_00424f80("hret!=0","E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                               DAT_005ff60c + 0xe,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (local_10 != 0x103) break;
      local_14 = local_14 + 1;
    }
    FUN_0042b2d0("ThreadKill():finish wait thread kill : %d\n",local_14);
    (*DAT_00592270)(param_1[7]);
    local_c = __chkesp();
    if ((local_c == 0) &&
       (iVar2 = FUN_00424f80("hret!=0","E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                             DAT_005ff60c + 0x15,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN_004225a0(0xffffffff);
    FUN_00421d50(param_1);
    if ((char)param_1[10] != '\0') {
      (**(code **)(*param_1 + 4))();
      __chkesp();
      local_18 = param_1;
      FUN_00428ad0(param_1);
    }
  }
  local_8 = 0x422285;
  __chkesp();
  return;
}

