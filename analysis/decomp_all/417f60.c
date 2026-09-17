
void __fastcall FUN__text__00417f60(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [12];
  undefined4 uStack_1c;
  int local_c;
  undefined4 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x5c) == '\0') {
    (*API_NTDLL_DLL_RtlInitializeCriticalSection)(param_1 + 0x51);
    FUN__text__0056ce80();
    *(undefined1 *)(local_8 + 0x5c) = 1;
  }
  (*API_COMBASE_DLL_CoCreateInstance)(&DAT_005cbe4c,0,1,&DAT_005cbe5c,local_8);
  local_c = FUN__text__0056ce80();
  if (-1 < local_c) {
    (*API_COMBASE_DLL_CoCreateInstance)(&DAT_005cbd8c,0,1,&DAT_005cbd9c,local_8 + 1);
    local_c = FUN__text__0056ce80();
    if ((-1 < local_c) && (local_c = FUN__text__00418110(), -1 < local_c)) {
      FUN__text__00418250();
      iVar1 = FUN__text__004194a0();
      if (iVar1 == 0) {
        (**(code **)(*(int *)*local_8 + 0x38))(*local_8,local_8 + 0x43,0);
        local_c = FUN__text__0056ce80();
        if (local_c == 0) {
          FUN__text__0042b2d0(&DAT_00592de8,local_8[0x45]);
        }
        goto LAB__text__00418097;
      }
    }
  }
  FUN__text__00417cc0();
LAB__text__00418097:
  uStack_1c = 0x4180a4;
  FUN__text__0056ce80();
  return;
}

