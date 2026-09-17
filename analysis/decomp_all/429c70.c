
void FUN__text__00429c70(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_458 [16];
  undefined1 local_418 [3];
  char local_415 [256];
  undefined1 local_315 [256];
  undefined1 local_215 [257];
  int local_114;
  int local_110;
  int local_10c;
  undefined1 local_108 [252];
  undefined4 uStack_c;
  
  puVar2 = local_458;
  for (iVar1 = 0x115; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_SHLWAPI_DLL_PathIsRelativeA)(param_1);
  iVar1 = FUN__text__0056ce80();
  if (iVar1 == 0) {
    (*API_KERNEL32_DLL_lstrcpyA)(local_108,param_1);
    FUN__text__0056ce80();
    (*API_SHLWAPI_DLL_PathStripToRootA)(local_108);
    local_10c = FUN__text__0056ce80();
    if (local_10c == 1) {
      (*API_KERNEL32_DLL_lstrlenA)(param_1);
      local_110 = FUN__text__0056ce80();
      if ((local_110 != 0) && (local_110 < 0x105)) {
        FUN__text__004296b0(param_1,local_418);
        (*API_KERNEL32_DLL_lstrlenA)(local_418);
        iVar1 = FUN__text__0056ce80();
        if ((iVar1 != 0) || (iVar1 = FUN__text__0042a030(param_1), iVar1 != 0)) {
          (*API_KERNEL32_DLL_lstrlenA)(local_415);
          iVar1 = FUN__text__0056ce80();
          if (iVar1 != 0) {
            (*API_KERNEL32_DLL_lstrlenA)(local_215);
            iVar1 = FUN__text__0056ce80();
            if (iVar1 != 0) {
              (*API_KERNEL32_DLL_lstrlenA)(local_315);
              iVar1 = FUN__text__0056ce80();
              if (iVar1 == 0) goto LAB__text__00429f27;
            }
            (*API_KERNEL32_DLL_lstrlenA)(local_418);
            local_110 = FUN__text__0056ce80();
            if ((local_110 == 0) || (iVar1 = FUN__text__00429be0(local_418), iVar1 != 0)) {
              (*API_KERNEL32_DLL_lstrlenA)(local_415);
              local_110 = FUN__text__0056ce80();
              if (local_110 != 0) {
                iVar1 = FUN__text__0042a030(param_1);
                if ((iVar1 == 0) && (iVar1 = FUN__text__004298e0(local_415), iVar1 != 0))
                goto LAB__text__00429f27;
                for (local_114 = 0; local_114 != local_110; local_114 = local_114 + 1) {
                  if (local_415[local_114] == '\\') {
                    local_415[local_114] = ' ';
                  }
                }
                iVar1 = FUN__text__00429b40(local_415);
                if (iVar1 == 0) goto LAB__text__00429f27;
              }
              FUN__text__0056d810(local_108,&DAT_00592b28,local_315,local_215);
              (*API_KERNEL32_DLL_lstrlenA)(local_108);
              local_110 = FUN__text__0056ce80();
              if (local_110 != 0) {
                FUN__text__00429aa0(local_108);
              }
            }
          }
        }
      }
    }
  }
LAB__text__00429f27:
  uStack_c = 0x429f37;
  FUN__text__0056ce80();
  return;
}

