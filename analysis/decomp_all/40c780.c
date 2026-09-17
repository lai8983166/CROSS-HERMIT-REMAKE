
void __thiscall FUN__text__0040c780(int param_1,int param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_260 [16];
  int local_220;
  int local_21c;
  int local_218;
  int local_214;
  undefined1 local_210 [260];
  undefined1 local_10c [260];
  int local_8;
  
  puVar3 = local_260;
  for (iVar2 = 0x97; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    FUN__text__0040d120(param_2);
    FUN__text__0040c1f0(param_2,0);
    local_214 = 0;
    local_220 = 0;
    while( true ) {
      (*API_KERNEL32_DLL_lstrlenA)(*(undefined4 *)(param_4 + local_214 * 4));
      local_21c = FUN__text__0056ce80();
      if (local_21c == 0) break;
      local_220 = local_220 + 1;
      local_214 = local_214 + 1;
    }
    (*API_KERNEL32_DLL_lstrlenA)(param_3);
    iVar2 = FUN__text__0056ce80();
    if (iVar2 != 0) {
      (*API_KERNEL32_DLL_lstrcpyA)(local_10c,param_3);
      FUN__text__0056ce80();
      FUN__text__004297a0(local_10c);
    }
    if (((param_2 < 0) || (0x13 < param_2)) &&
       (iVar2 = FUN__text__00424f80("(0<=no)&&(no<20)",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff12c + 0x18,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (((local_220 < 0) || (0x77 < local_220)) &&
       (iVar2 = FUN__text__00424f80("(0<=rcnt)&&(rcnt<120)",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff12c + 0x19,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    for (local_214 = 0; local_214 != local_220; local_214 = local_214 + 1) {
      FUN__text__0056d810(local_210,&DAT_00592a18,*(undefined4 *)(param_4 + local_214 * 4));
      local_218 = FUN__text__0040cf00(local_8 + 0x14 + param_2 * 0x5a0 + local_214 * 0xc,local_210);
      if (local_218 != 0) {
        FUN__text__0040d120(param_2);
        break;
      }
    }
  }
  local_8 = 0x40c9ad;
  FUN__text__0056ce80();
  return;
}

