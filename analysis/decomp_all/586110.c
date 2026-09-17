
int FUN__text__00586110(void)

{
  int local_10;
  int local_c;
  undefined4 *local_8;
  
  local_c = -1;
  FUN__text__00577040(0x12);
  local_10 = 0;
  do {
    if (0x3f < local_10) {
LAB__text__005862e0:
      FUN__text__005770e0(0x12);
      return local_c;
    }
    if ((&DAT_0080a800)[local_10] == 0) {
      local_8 = (undefined4 *)__malloc_dbg(0x480,2,"osfinfo.c",0x79);
      if (local_8 != (undefined4 *)0x0) {
        (&DAT_0080a800)[local_10] = local_8;
        DAT_0080a900 = DAT_0080a900 + 0x20;
        for (; local_8 < (undefined4 *)((&DAT_0080a800)[local_10] + 0x480); local_8 = local_8 + 9) {
          *(undefined1 *)(local_8 + 1) = 0;
          *local_8 = 0xffffffff;
          *(undefined1 *)((int)local_8 + 5) = 10;
          local_8[2] = 0;
        }
        local_c = local_10 << 5;
        FUN__text__00586620(local_c);
      }
      goto LAB__text__005862e0;
    }
    for (local_8 = (undefined4 *)(&DAT_0080a800)[local_10];
        local_8 < (undefined4 *)((&DAT_0080a800)[local_10] + 0x480); local_8 = local_8 + 9) {
      if ((*(byte *)(local_8 + 1) & 1) == 0) {
        if (local_8[2] == 0) {
          FUN__text__00577040(0x11);
          if (local_8[2] == 0) {
            (*API_NTDLL_DLL_RtlInitializeCriticalSection)(local_8 + 3);
            local_8[2] = local_8[2] + 1;
          }
          FUN__text__005770e0(0x11);
        }
        (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_8 + 3);
        if ((*(byte *)(local_8 + 1) & 1) == 0) {
          *local_8 = 0xffffffff;
          local_c = local_10 * 0x20 + ((int)local_8 - (&DAT_0080a800)[local_10]) / 0x24;
          break;
        }
        (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_8 + 3);
      }
    }
    if (local_c != -1) goto LAB__text__005862e0;
    local_10 = local_10 + 1;
  } while( true );
}

