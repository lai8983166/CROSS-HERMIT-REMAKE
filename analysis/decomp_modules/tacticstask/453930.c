
void FUN__text__00453930(void)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00496450();
  if (iVar2 == 0) {
    uVar1 = FUN__text__0041ad60();
    *(undefined1 *)(local_8 + 0x2f0d4) = uVar1;
  }
  DAT_007f448c._3_1_ = 0;
  *(undefined4 *)(local_8 + 0x34) = 2;
  local_8 = 0x45399f;
  FUN__text__0056ce80();
  return;
}

