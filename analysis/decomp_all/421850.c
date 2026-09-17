
void thread_sync_helper(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_60 [16];
  int *piStack_20;
  int iStack_1c;
  int iStack_18;
  int iStack_14;
  int iStack_10;
  uint uStack_c;
  undefined *puStack_8;
  
  puVar3 = auStack_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uStack_c = func_0x004225e0();
  if ((uStack_c & 2) != 0) goto code_r0x00421bd0;
  if ((uStack_c & 1) == 0) {
    (*API_KERNEL32_DLL_CreateEventA)(0,0,0,0);
    iVar2 = __chkesp();
    param_1[7] = iVar2;
    if (param_1[7] == 0) {
      FUN_0042b2d0("ERROR:TaskExecSub():CreateEvent:dont create event !!\n");
      iVar2 = FUN_00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                           DAT_005ff5f8 + 0x1d,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto code_r0x00421bd0;
    }
    iStack_10 = func_0x00421ea0(param_1);
    if (iStack_10 != 0) {
      FUN_0042b2d0("ERROR:TaskExecSub():ThreadCreate:dont create thread !!\n");
      iVar2 = FUN_00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                           DAT_005ff5f8 + 0x25,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto code_r0x00421bd0;
    }
    (*API_NTDLL_DLL_RtlEnterCriticalSection)((int)puStack_8 + 0x100);
    __chkesp();
    func_0x00422560(1);
    (*API_KERNEL32_DLL_ResetEvent)(*(undefined4 *)((int)puStack_8 + 0x118));
    __chkesp();
    (*API_KERNEL32_DLL_SetEvent)(param_1[7]);
    __chkesp();
    (*API_KERNEL32_DLL_ResumeThread)(param_1[8]);
    __chkesp();
    (*API_NTDLL_DLL_RtlLeaveCriticalSection)((int)puStack_8 + 0x100);
    __chkesp();
    (*API_KERNEL32_DLL_WaitForSingleObject)(*(undefined4 *)((int)puStack_8 + 0x118),0xffffffff);
    __chkesp();
  }
  else {
    if (param_1[5] != 0) {
      param_1[5] = param_1[5] + -1;
      goto code_r0x00421bd0;
    }
    (*API_NTDLL_DLL_RtlEnterCriticalSection)((int)puStack_8 + 0x100);
    __chkesp();
    func_0x00422560(1);
    (*API_KERNEL32_DLL_ResetEvent)(*(undefined4 *)((int)puStack_8 + 0x118));
    __chkesp();
    (*API_KERNEL32_DLL_SetEvent)(param_1[7]);
    __chkesp();
    (*API_NTDLL_DLL_RtlLeaveCriticalSection)((int)puStack_8 + 0x100);
    __chkesp();
    (*API_KERNEL32_DLL_WaitForSingleObject)(*(undefined4 *)((int)puStack_8 + 0x118),0xffffffff);
    __chkesp();
  }
  uStack_c = func_0x004225e0();
  if ((uStack_c & 4) != 0) {
    iStack_1c = 0;
    while( true ) {
      (*DAT_00592264)(2);
      __chkesp();
      (*API_KERNEL32_DLL_GetExitCodeThread)(param_1[8],&iStack_18);
      iStack_14 = __chkesp();
      if ((iStack_14 == 0) &&
         (iVar2 = FUN_00424f80("hret!=0","E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                               DAT_005ff5f8 + 0x40,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (iStack_18 != 0x103) break;
      iStack_1c = iStack_1c + 1;
    }
    FUN_0042b2d0("ThreadKill():finish wait thread kill : %d\n",iStack_1c);
    (*DAT_00592270)(param_1[7]);
    iStack_14 = __chkesp();
    if ((iStack_14 == 0) &&
       (iVar2 = FUN_00424f80("hret!=0","E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                             DAT_005ff5f8 + 0x4c,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN_004225a0(0xffffffff);
    FUN_00421d50(param_1);
    if ((char)param_1[10] != '\0') {
      (**(code **)(*param_1 + 4))();
      __chkesp();
      piStack_20 = param_1;
      FUN_00428ad0(param_1);
    }
  }
code_r0x00421bd0:
  puStack_8 = &UNK_00421bdd;
  __chkesp();
  return;
}

