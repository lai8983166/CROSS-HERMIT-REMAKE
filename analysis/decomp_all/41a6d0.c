
void __fastcall FUN_0041a6d0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x13c) != 0) {
    local_8 = param_1;
    (*DAT_00592260)(*(undefined4 *)(param_1 + 0x13c),0);
    local_c = __chkesp();
    if (local_c == 0) {
      iVar2 = FUN_00424f80("ret!=0","E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                           DAT_005ff588 + 7,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    while( true ) {
      (*DAT_00592264)(100);
      __chkesp();
      (*API_KERNEL32_DLL_GetExitCodeThread)(*(undefined4 *)(local_8 + 0x13c),&local_10);
      local_c = __chkesp();
      if (local_c == 0) {
        iVar2 = FUN_00424f80("ret!=0","E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                             DAT_005ff588 + 0xc,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      if (local_10 != 0x103) break;
      FUN_0042b2d0("DeleteReciveThread():wait thread kill\n");
    }
    (*DAT_00592270)(*(undefined4 *)(local_8 + 0x13c));
    local_c = __chkesp();
    *(undefined4 *)(local_8 + 0x13c) = 0;
  }
  local_8 = 0x41a7fb;
  __chkesp();
  return;
}

