
void FUN__text__0046ea10(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [16];
  uint local_2c;
  int local_28;
  undefined4 local_24;
  undefined4 local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  iVar1 = FUN__text__00493670();
  if (((iVar1 != 0) ||
      ((local_18 = FUN__text__004945b0(), local_18 != -1 &&
       (iVar1 = FUN__text__004942b0(local_18), iVar1 != 0)))) ||
     ((iVar1 = FUN__text__004947b0(), iVar1 != -1 && (iVar1 = FUN__text__004948f0(), iVar1 != 0))))
  goto LAB__text__0046ec68;
  if (((*(int *)(local_8 + 0x2a340) == 1) && ((*(uint *)(DAT_007a49fc + 0x1990) & 8) != 0)) ||
     ((*(int *)(local_8 + 0x2a340) == 1 &&
      ((((*(uint *)(DAT_007a49fc + 0x1990) & 0x40) != 0 &&
        ((*(uint *)(DAT_007a49fc + 0x194c) & 0x40000) == 0)) &&
       (*(char *)(local_8 + 0x108b36) != '\0')))))) {
LAB__text__0046eb54:
    local_14 = 0;
  }
  else {
    if ((*(int *)(local_8 + 0x2a340) != 1) || (*(int *)(DAT_007a49fc + 0x19b8) != 3))
    goto LAB__text__0046ec68;
    local_10 = 1;
    if ((*(int *)(DAT_007a49fc + 0x19bc) == *(int *)(DAT_007a49fc + 0x19c8)) &&
       (*(int *)(DAT_007a49fc + 0x19c0) == *(int *)(DAT_007a49fc + 0x19cc)))
    goto LAB__text__0046eb54;
    local_14 = 1;
  }
  if (((*(uint *)(DAT_007a49fc + 0x194c) & 0x40000) == 0) && (*(char *)(local_8 + 0x108b36) != '\0')
     ) {
    for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
      iVar1 = FUN__text__0046a4c0(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
      if (iVar1 != 0) {
        *(undefined1 *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 600) + 0x9d) = 0;
      }
      *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 0x28c) = 0;
    }
  }
  *(undefined4 *)(local_8 + 0x108f74) = 0;
  local_24 = 0;
  local_20 = 0;
  if ((*(char *)(local_8 + 0x108b36) != '\0') &&
     (((local_1c = FUN__text__0046f8b0(local_14), local_1c == 0 ||
       (iVar1 = FUN__text__0046eda0(local_14,local_1c), iVar1 == 0)) &&
      (*(char *)(local_8 + 0x108b37) != '\x01')))) {
    FUN__text__0046efa0(local_14,local_1c);
  }
LAB__text__0046ec68:
  FUN__text__0046f170();
  if (local_10 != 0) {
    for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
      iVar1 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
      if (iVar1 != 0) {
        local_2c = (uint)*(byte *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 600) + 0xf)
        ;
        switch(local_2c) {
        case 0:
        case 1:
        case 2:
          FUN__text__0049ad90(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4),0x97);
          break;
        case 3:
          FUN__text__0049ad90(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4),0x96);
          break;
        case 4:
        case 5:
        }
      }
    }
  }
  local_28 = FUN__text__00494620();
  if (local_28 != -1) {
    FUN__text__00494030(local_28);
  }
  local_8 = 0x46ed7f;
  FUN__text__0056ce80();
  return;
}

