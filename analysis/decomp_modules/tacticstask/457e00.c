
void FUN__text__00457e00(undefined1 param_1,undefined1 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_e8 [16];
  int local_a8;
  int local_a4;
  undefined4 local_a0;
  undefined1 local_9c [13];
  undefined1 local_8f;
  undefined1 local_8c;
  undefined1 local_8b;
  undefined1 local_8a [126];
  undefined4 uStack_c;
  
  puVar2 = local_e8;
  for (iVar1 = 0x39; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_lstrlenA)(param_3);
  local_a4 = FUN__text__0056ce80();
  if ((local_a4 != 0) && (local_a4 < 0x7f)) {
    _memset(local_9c,0,0x94);
    local_8f = 0xb;
    local_8c = param_1;
    local_8b = param_2;
    (*API_KERNEL32_DLL_lstrcpyA)(local_8a,param_3);
    FUN__text__0056ce80();
    local_a8 = local_a4 + 0x16;
    iVar1 = FUN__text__00419450();
    if (iVar1 == 0) {
      local_a0 = FUN__text__00419f90(local_9c,local_a8);
    }
    else {
      local_a0 = FUN__text__00419fe0(local_9c,local_a8);
    }
  }
  uStack_c = 0x457f48;
  FUN__text__0056ce80();
  return;
}

