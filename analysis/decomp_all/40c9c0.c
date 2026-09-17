
void FUN__text__0040c9c0(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  void *local_28;
  int local_24;
  int *local_20;
  void *local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  undefined4 local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  local_18 = 0;
  while( true ) {
    (*API_KERNEL32_DLL_lstrlenA)(*(undefined4 *)(param_1 + local_10 * 4));
    local_14 = FUN__text__0056ce80();
    if (local_14 == 0) break;
    local_18 = local_18 + 1;
    local_10 = local_10 + 1;
  }
  if (local_18 != 0) {
    local_20 = (int *)FUN__text__00428a40(8);
    local_c = local_20;
    if ((local_20 == (int *)0x0) &&
       (iVar2 = FUN__text__00424f80("tbl!=0",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff130 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *local_c = local_18;
    local_24 = FUN__text__00428a40(*local_c << 2);
    local_c[1] = local_24;
    if ((local_c[1] == 0) &&
       (iVar2 = FUN__text__00424f80("tbl->rtbl != 0",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff130 + 0x11,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_c[1] == 0) {
LAB__text__0040cb9c:
      FUN__text__0040cbd0(local_c);
    }
    else {
      _memset((void *)local_c[1],0,*local_c << 2);
      for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
        local_28 = (void *)FUN__text__00428a40(0x104);
        local_1c = local_28;
        if ((local_28 == (void *)0x0) &&
           (iVar2 = FUN__text__00424f80("addr != 0",
                                        "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                        DAT_005ff130 + 0x18,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        if (local_1c == (void *)0x0) goto LAB__text__0040cb9c;
        _memset(local_1c,0,0x104);
        FUN__text__0056d810(local_1c,&DAT_00592b28,param_2,*(undefined4 *)(param_1 + local_10 * 4));
        *(void **)(local_c[1] + local_10 * 4) = local_1c;
      }
    }
  }
  local_8 = 0x40cbbd;
  FUN__text__0056ce80();
  return;
}

