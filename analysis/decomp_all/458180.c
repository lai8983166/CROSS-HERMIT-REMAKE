
void FUN__text__00458180(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if ((((iVar1 != 0) && (iVar1 = FUN__text__00454c40(), iVar1 == 0)) &&
      (*(int *)(local_8 + 0x38) == 5)) &&
     (((iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x196c),
                                    *(undefined4 *)(DAT_007a49fc + 0x1970),0x3d2,0x2c4,0x2a,0x2a),
       iVar1 != 0 &&
       (iVar1 = FUN__text__0042b0d0(*(undefined4 *)(DAT_007a49fc + 0x19bc),
                                    *(undefined4 *)(DAT_007a49fc + 0x19c0),0x3d2,0x2c4,0x2a,0x2a),
       iVar1 != 0)) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)))) {
    *(byte *)(local_8 + 0x18d) = *(byte *)(local_8 + 0x18d) ^ 1;
  }
  local_8 = 0x458276;
  FUN__text__0056ce80();
  return;
}

