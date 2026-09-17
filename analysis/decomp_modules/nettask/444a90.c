
void __fastcall FUN__text__00444a90(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  (*API_KERNEL32_DLL_lstrcpyA)(param_1 + 0x1a60,"PlayerName ");
  FUN__text__0056ce80();
  FUN__text__00425a10();
  FUN__text__004262a0(0xf);
  FUN__text__00426310(local_8 + 0x1a60);
  FUN__text__00425ed0(1);
  FUN__text__0044ca80();
  FUN__text__0044c9a0(0);
  FUN__text__00422360(0);
  _memset((void *)(local_8 + 0x1bb0),0,0x10);
  local_10 = 1;
  do {
    if (local_10 == 0) {
      FUN__text__00425ed0(0);
      local_10 = 0x444d31;
      FUN__text__0056ce80();
      return;
    }
    local_c = FUN__text__0044c710(&DAT_00605a48,2);
    iVar2 = FUN__text__004263b0(DAT_007a49fc);
    if (iVar2 == 0) {
      if ((local_c != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
        local_1c = local_c;
        if (local_c == 0) goto LAB__text__00444bcd;
        if (local_c == 1) {
          *(undefined4 *)(local_8 + 0x1a50) = 2;
          FUN__text__004db2b0(2);
          local_10 = 0;
        }
      }
    }
    else {
LAB__text__00444bcd:
      uVar1 = FUN__text__004264d0();
      (*API_KERNEL32_DLL_lstrlenA)(uVar1);
      iVar2 = FUN__text__0056ce80();
      if (iVar2 != 0) {
        *(undefined4 *)(local_8 + 0x1a50) = 6;
        uVar1 = FUN__text__004264d0();
        (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0x1a60,uVar1);
        FUN__text__0056ce80();
        (*API_KERNEL32_DLL_lstrcpyA)("PlayerName ",local_8 + 0x1a60);
        FUN__text__0056ce80();
        FUN__text__004db2b0(5);
        local_10 = 0;
      }
    }
    if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
      local_c = -1;
    }
    FUN__text__00444d40(local_c,0xff);
    FUN__text__0044ca80();
    FUN__text__0044c9a0(0);
    local_14 = 0x1bd;
    local_18 = 0x171;
    FUN__text__00426820(DAT_007a49fc,0x1bd,0x171,0x12,0,local_8 + 0xdb8,local_8 + 0xe44,0x54);
    FUN__text__00422360(0);
  } while( true );
}

