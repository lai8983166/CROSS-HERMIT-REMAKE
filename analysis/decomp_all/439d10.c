
void __fastcall FUN__text__00439d10(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _memset(param_1 + 7,0,8);
  local_8[8] = 0xffffffff;
  local_8[7] = 0;
  (*API_NTDLL_DLL_RtlInitializeCriticalSection)(local_8 + 1);
  FUN__text__0056ce80();
  *local_8 = 1;
  uStack_c = 0x439d83;
  FUN__text__0056ce80();
  return;
}

