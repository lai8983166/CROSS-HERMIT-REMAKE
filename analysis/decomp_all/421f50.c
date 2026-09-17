
/* WARNING: Removing unreachable block (ram,0x00422072) */

void FUN__text__00421f50(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  local_c = param_1[2];
  (**(code **)*param_1)(param_1[6]);
  FUN__text__0056ce80();
  FUN__text__0042b2d0("ThreadStart():end thread start\n");
  (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  FUN__text__004225a0(0xffffffff);
  FUN__text__00422560(4);
  (*API_KERNEL32_DLL_ResetEvent)(local_8[7]);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_SetEvent)(*(undefined4 *)(local_c + 0x118));
  FUN__text__0056ce80();
  (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  FUN__text__0042b2d0("ThreadStart(%08x):thread dead\n");
  __endthreadex(0);
  do {
    FUN__text__0042b2d0("ERROR:ThreadStart(%08x):thread already alived !!\n",local_8);
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff608 + 0x27,0);
  } while (iVar2 == 0);
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

