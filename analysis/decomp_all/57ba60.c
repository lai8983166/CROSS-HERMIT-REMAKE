
void FUN__text__0057ba60(void)

{
  undefined **local_10;
  int local_c;
  int local_8;
  
  if (DAT_0080ab2c == 3) {
    local_c = DAT_0080ab48;
    for (local_8 = 0; local_8 < DAT_0080ab44; local_8 = local_8 + 1) {
      (*API_KERNEL32_DLL_VirtualFree)(*(undefined4 *)(local_c + 0xc),0x100000,0x4000);
      (*API_KERNEL32_DLL_VirtualFree)(*(undefined4 *)(local_c + 0xc),0,0x8000);
      (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,*(undefined4 *)(local_c + 0x10));
      local_c = local_c + 0x14;
    }
    (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,DAT_0080ab48);
  }
  else if (DAT_0080ab2c == 2) {
    local_10 = &PTR_LOOP_00762138;
    do {
      if (local_10[4] != (undefined *)0x0) {
        (*API_KERNEL32_DLL_VirtualFree)(local_10[4],0,0x8000);
      }
      local_10 = (undefined **)*local_10;
    } while (local_10 != &PTR_LOOP_00762138);
  }
  (*API_KERNEL32_DLL_HeapDestroy)(DAT_0080ab28);
  return;
}

