
void FUN__text__00491680(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00454c40();
  if (iVar1 == 0) {
    local_18 = (int)*(char *)(local_8 + 0x30994);
    switch(local_18) {
    case 0:
      local_14 = 0x226;
      break;
    case 1:
      local_14 = 0x227;
      break;
    case 2:
      local_14 = 0x228;
      break;
    case 3:
      local_14 = 0x229;
      break;
    case 4:
      local_14 = 0x22a;
      break;
    case 5:
      local_14 = 0x22b;
      break;
    case 6:
      local_14 = 0x22c;
      break;
    case 7:
      local_14 = 0x22d;
      break;
    case 8:
      local_14 = 0x22e;
      break;
    case 9:
      local_14 = 0x22f;
      break;
    case 10:
      local_14 = 0x230;
    }
    local_c = *(short *)(DAT_007a49fc + 0x196c);
    local_10 = *(short *)(DAT_007a49fc + 0x1970);
    if (*(char *)(local_8 + 0x30995) != '\0') {
      FUN__text__004077c0(DAT_007a49fc);
      *(undefined2 *)(local_8 + 0xde808) = 0;
      FUN__text__00407870(0x5a,0x231);
      *(undefined4 *)(local_8 + 0xde80c) = 0;
      *(undefined2 *)(local_8 + 0xde826) = 1;
      *(undefined1 *)(local_8 + 0xde817) = 0xff;
      *(undefined1 *)(local_8 + 0xde814) = 0x80;
      *(undefined1 *)(local_8 + 0xde815) = 0x80;
      *(undefined1 *)(local_8 + 0xde816) = 0x80;
      FUN__text__004079c0((int)local_c,(int)local_10);
    }
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0xde808) = 0;
    FUN__text__00407870(0x5a,local_14);
    *(undefined4 *)(local_8 + 0xde80c) = 0;
    *(undefined2 *)(local_8 + 0xde826) = 1;
    *(undefined1 *)(local_8 + 0xde817) = 0xff;
    *(undefined1 *)(local_8 + 0xde814) = 0x80;
    *(undefined1 *)(local_8 + 0xde815) = 0x80;
    *(undefined1 *)(local_8 + 0xde816) = 0x80;
    FUN__text__004079c0((int)local_c,(int)local_10);
  }
  local_8 = 0x49188f;
  FUN__text__0056ce80();
  return;
}

