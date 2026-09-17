
/* WARNING: Removing unreachable block (ram,0x00422543) */

void __fastcall FUN__text__00422440(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 8);
  local_8 = param_1;
  (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  FUN__text__004225a0(0xffffffff);
  FUN__text__00422560(4);
  (*API_KERNEL32_DLL_ResetEvent)(*(undefined4 *)(local_8 + 0x1c));
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_SetEvent)(*(undefined4 *)(local_c + 0x118));
  FUN__text__0056ce80();
  FUN__text__0042b2d0("TaskKill(%08x):thread kill\n",local_8);
  (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  __endthreadex(0);
  do {
    FUN__text__0042b2d0("ERROR:TaskKill(%08x):thread already alived !!\n",local_8);
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff610 + 0xe,0);
  } while (iVar2 == 0);
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

