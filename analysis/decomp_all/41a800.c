
/* WARNING: Removing unreachable block (ram,0x0041aae8) */

void FUN__text__0041a800(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  undefined4 local_18;
  int local_14;
  undefined4 local_10;
  int *local_c;
  undefined4 *local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_1[9] == 0) &&
     (iVar2 = FUN__text__00424f80("work->pDxPlay!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff58c + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((local_8[10] == 0) &&
     (iVar2 = FUN__text__00424f80("work->hEvent!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff58c + 8,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((local_8[0xb] == 0) &&
     (iVar2 = FUN__text__00424f80("work->mem!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff58c + 10,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (int *)local_8[0xb];
  do {
    (*API_KERNEL32_DLL_WaitForSingleObject)(local_8[10],0xffffffff);
    iVar2 = FUN__text__0056ce80();
    if (iVar2 != 0) {
      (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_8 + 2);
      FUN__text__0056ce80();
      FUN__text__0042b2d0("ReceiveThread(%08x):thread dead\n",*local_8);
      (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_8 + 2);
      FUN__text__0056ce80();
      __endthreadex(0);
      do {
        FUN__text__0042b2d0("ERROR:ReceiveThread(%08x):thread already alived !!\n",*local_8);
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                    DAT_005ff58c + 0x49,0);
      } while (iVar2 == 0);
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = 0;
    do {
      (**(code **)(*(int *)local_8[9] + 100))(local_8[9],&local_14,&local_18,1,0,&local_10);
      local_1c = FUN__text__0056ce80();
      if (local_1c != -0x7788ffe2) break;
      if (*local_c != 0) {
        local_20 = *local_c;
        FUN__text__00428ad0(local_20);
        *local_c = 0;
      }
      while( true ) {
        local_24 = FUN__text__00428a40(local_10);
        *local_c = local_24;
        if (*local_c != 0) break;
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                    DAT_005ff58c + 0x21,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      (**(code **)(*(int *)local_8[9] + 100))(local_8[9],&local_14,&local_18,1,*local_c,&local_10);
      local_1c = FUN__text__0056ce80();
      if (local_1c < 0) break;
      if (local_14 == 0) {
        FUN__text__0041b200(0,local_18,*local_c);
      }
      if (local_8[8] != 0) {
        (*(code *)local_8[8])(local_14,local_18,*local_c,local_10);
        FUN__text__0056ce80();
      }
      if (*local_c != 0) {
        local_28 = *local_c;
        FUN__text__00428ad0(local_28);
        *local_c = 0;
      }
    } while (-1 < local_1c);
  } while( true );
}

