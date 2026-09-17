
void __fastcall FUN__text__00421540(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_48 [11];
  undefined4 uStack_1c;
  int local_8;
  
  puVar4 = local_48;
  for (iVar3 = 0x11; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  (*API_NTDLL_DLL_RtlInitializeCriticalSection)(param_1 + 0x100);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_CreateEventA)(0,0,0,0);
  uVar2 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x118) = uVar2;
  if (*(int *)(local_8 + 0x118) == 0) {
    FUN__text__0042b2d0("ERROR:SysTaskCtrl():CreateEvent:dont create event !!\n");
    iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff5f0 + 7,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_1c = 0x4215eb;
  FUN__text__0056ce80();
  return;
}

