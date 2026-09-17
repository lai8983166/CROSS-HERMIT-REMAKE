
void FUN__text__00430260(void)

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
  local_c = *(undefined4 *)(DAT_007a49fc + 0x196c);
  local_10 = *(undefined4 *)(DAT_007a49fc + 0x1970);
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x94) = 0x80;
  *(undefined4 *)(local_8 + 0x98) = 0;
  *(undefined1 *)(local_8 + 0xa3) = 0xff;
  *(undefined1 *)(local_8 + 0xa0) = 0x80;
  *(undefined1 *)(local_8 + 0xa1) = 0x80;
  *(undefined1 *)(local_8 + 0xa2) = 0x80;
  *(undefined2 *)(local_8 + 0xb2) = 1;
  FUN__text__00407870(0x5a,0);
  FUN__text__004079c0(local_c,local_10);
  local_8 = 0x430328;
  FUN__text__0056ce80();
  return;
}

