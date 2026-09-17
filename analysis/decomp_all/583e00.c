
int FUN__text__00583e00(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  int local_10;
  uint local_c;
  
  if ((param_2 != 4) && (param_2 != 3)) {
    if ((param_1 == 2) || (((param_1 == 0x15 || (param_1 == 0x16)) || (param_1 == 0xf)))) {
      FUN__text__00577040(1);
      if (((param_1 == 2) || (param_1 == 0x15)) && (DAT_0080a69c == 0)) {
        iVar2 = (*API_KERNEL32_DLL_SetConsoleCtrlHandler)(FUN__text__00584030,1);
        if (iVar2 != 1) {
          uVar3 = (*API_KERNEL32_DLL_GetLastError)();
          puVar4 = (undefined4 *)FUN__text__00576d30();
          *puVar4 = uVar3;
          FUN__text__005770e0(1);
          goto LAB__text__00583fe8;
        }
        DAT_0080a69c = 1;
      }
      switch(param_1) {
      case 2:
        local_10 = DAT_0080a68c;
        DAT_0080a68c = param_2;
        break;
      case 0xf:
        local_10 = DAT_0080a698;
        DAT_0080a698 = param_2;
        break;
      case 0x15:
        local_10 = DAT_0080a690;
        DAT_0080a690 = param_2;
        break;
      case 0x16:
        local_10 = DAT_0080a694;
        DAT_0080a694 = param_2;
      }
      FUN__text__005770e0(1);
      return local_10;
    }
    if (((param_1 == 8) || (param_1 == 4)) || (param_1 == 0xb)) {
      iVar2 = FUN__text__005753b0();
      if (*(undefined **)(iVar2 + 0x50) == &DAT_00761d68) {
        uVar3 = __malloc_dbg(DAT_00761de8,2,"winsig.c",0x133);
        *(undefined4 *)(iVar2 + 0x50) = uVar3;
        if (*(int *)(iVar2 + 0x50) == 0) goto LAB__text__00583fe8;
        FUN__text__0056d4d0(*(undefined4 *)(iVar2 + 0x50),&DAT_00761d68,DAT_00761de8);
      }
      local_c = FUN__text__00584310(param_1,*(undefined4 *)(iVar2 + 0x50));
      if (local_c != 0) {
        iVar1 = *(int *)(local_c + 8);
        do {
          if (*(int *)(local_c + 4) != param_1) {
            return iVar1;
          }
          *(int *)(local_c + 8) = param_2;
          local_c = local_c + 0xc;
        } while (local_c < (uint)(*(int *)(iVar2 + 0x50) + DAT_00761dec * 0xc));
        return iVar1;
      }
    }
  }
LAB__text__00583fe8:
  puVar4 = (undefined4 *)FUN__text__00576d20();
  *puVar4 = 0x16;
  return -1;
}

