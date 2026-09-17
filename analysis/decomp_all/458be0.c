
void __fastcall FUN__text__00458be0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  *(undefined1 *)(param_1 + 0x11804c) = 0;
  local_8 = param_1;
  iVar1 = FUN__text__00456b20();
  if ((((iVar1 == 0) && (iVar1 = FUN__text__00454c40(), iVar1 == 0)) &&
      (*(int *)(local_8 + 0x38) == 5)) && (iVar1 = FUN__text__004577f0(), iVar1 == 0)) {
    iVar1 = FUN__text__004128f0(0x39,1);
    if (iVar1 == 0) {
      iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                  *(undefined4 *)(DAT_007a49fc + 0x1970),0x3d1,0x26f,0x33,0x28);
      if (iVar1 != 0) {
        local_c = 1;
      }
      if (((*(int *)(DAT_007a49fc + 0x19b8) != 3) || (local_c == 0)) ||
         ((iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x19bc),
                                       *(undefined4 *)(DAT_007a49fc + 0x19c0),0x3d1,0x26f,0x33,0x28)
          , iVar1 == 0 || ((*(uint *)(DAT_007a49fc + 0x199c) & 1) == 0)))) goto LAB__text__00458d5e;
    }
    if (*(char *)(local_8 + 0x30b28) == '\0') {
      FUN__text__004998b0(*(char *)(*(int *)(local_8 + 0x60) + 3) + 7);
      FUN__text__004db2b0(5);
      *(undefined1 *)(local_8 + 0x30) = 2;
    }
  }
LAB__text__00458d5e:
  local_8 = 0x458d6b;
  FUN__text__0056ce80();
  return;
}

