
void __fastcall FUN__text__004816c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = *(int *)(DAT_007a49fc + 0x19b8);
  local_8 = param_1;
  if (local_18 == 0) {
    if (*(char *)(param_1 + 0x2f15b) != '\0') {
      FUN__text__00481580();
    }
  }
  else if (local_18 == 1) {
    local_c = FUN__text__0046f8b0(0);
    if ((local_c != 0) && (iVar1 = FUN__text__004818e0(0,local_c), iVar1 != 0)) {
      *(undefined1 *)(local_8 + 0x2f15b) = 1;
    }
  }
  else if ((local_18 == 2) && (*(char *)(param_1 + 0x2f15b) != '\0')) {
    local_10 = FUN__text__0056db00(*(int *)(DAT_007a49fc + 0x19bc) - *(int *)(DAT_007a49fc + 0x196c)
                                  );
    local_14 = FUN__text__0056db00(*(int *)(DAT_007a49fc + 0x19c0) - *(int *)(DAT_007a49fc + 0x1970)
                                  );
    iVar1 = FUN__text__00412810(local_10,local_14);
    if (iVar1 != 0) {
      FUN__text__00481a60();
      FUN__text__00481ef0(0);
      *(undefined4 *)(local_8 + 0x2a344) = 0;
      *(undefined1 *)(local_8 + 0x2f15b) = 2;
    }
  }
  local_8 = 0x481800;
  FUN__text__0056ce80();
  return;
}

