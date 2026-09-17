
void FUN_004215f0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [14];
  undefined4 uStack_10;
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_00421bf0();
  (*API_NTDLL_DLL_RtlDeleteCriticalSection)(local_8 + 0x100);
  __chkesp();
  (*DAT_00592270)(*(undefined4 *)(local_8 + 0x118));
  __chkesp();
  uStack_10 = 0x421653;
  __chkesp();
  return;
}

