
void FUN__text__00457890(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if (((iVar1 != 0) && (iVar1 = FUN__text__00454c40(), iVar1 == 0)) &&
     (*(int *)(local_8 + 0x38) == 5)) {
    iVar1 = FUN__text__004128f0(0x1c,1);
    if (iVar1 == 0) {
      iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                  *(undefined4 *)(DAT_007a49fc + 0x1970),0x3d2,0x298,0x2a,0x2a);
      if (((iVar1 != 0) &&
          (iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x19bc),
                                       *(undefined4 *)(DAT_007a49fc + 0x19c0),0x3d2,0x298,0x2a,0x2a)
          , iVar1 != 0)) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
        *(byte *)(local_8 + 0x18c) = *(byte *)(local_8 + 0x18c) ^ 1;
      }
    }
    else {
      iVar1 = FUN__text__004577f0();
      if (iVar1 == 0) {
        *(undefined1 *)(local_8 + 0x117f20) = 1;
        FUN__text__00425a10();
        FUN__text__004262a0(0x36);
        FUN__text__00425ed0(1);
      }
      else {
        local_c = FUN__text__004264d0();
        local_10 = FUN__text__00426160();
        (*API_KERNEL32_DLL_lstrlenA)(local_c);
        iVar1 = FUN__text__0056ce80();
        if (iVar1 == 0) {
          (*API_KERNEL32_DLL_lstrlenA)(local_10);
          iVar1 = FUN__text__0056ce80();
          if (iVar1 == 0) {
            FUN__text__00425ed0(0);
            FUN__text__00425a10();
            *(undefined1 *)(local_8 + 0x117f20) = 0;
          }
        }
      }
    }
  }
  local_8 = 0x457a98;
  FUN__text__0056ce80();
  return;
}

