
void FUN__text__00458580(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if ((((iVar1 != 0) || (iVar1 = FUN__text__00454c40(), iVar1 != 0)) ||
      (*(int *)(local_8 + 0x38) != 5)) || (iVar1 = FUN__text__004577f0(), iVar1 != 0))
  goto LAB__text__004586b6;
  iVar1 = FUN__text__004128f0(1,1);
  if (iVar1 == 0) {
    if (*(int *)(DAT_007a49fc + 0x19b8) != 3) goto LAB__text__004586b6;
    local_c = *(int *)(DAT_007a49fc + 0x196c);
    local_10 = *(int *)(DAT_007a49fc + 0x1970);
    local_14 = *(int *)(DAT_007a49fc + 0x19bc);
    local_18 = *(int *)(DAT_007a49fc + 0x19c0);
    if (((((local_c < 9) || (0x58 < local_c)) ||
         ((local_10 < 3 || ((0x18 < local_10 || (local_14 < 9)))))) || (0x58 < local_14)) ||
       (((local_18 < 3 || (0x18 < local_18)) || ((*(uint *)(DAT_007a49fc + 0x199c) & 1) == 0))))
    goto LAB__text__004586b6;
  }
  FUN__text__004db2b0(5);
  *(undefined1 *)(local_8 + 0x30) = 1;
LAB__text__004586b6:
  local_8 = 0x4586c3;
  FUN__text__0056ce80();
  return;
}

