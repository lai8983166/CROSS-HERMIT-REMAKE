
void FUN__text__0045ecc0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__0045edf0();
  local_c = local_10;
  switch(local_10) {
  case 0:
    FUN__text__004e1b60();
    FUN__text__00439e30(7);
    break;
  case 1:
    FUN__text__004e1b60();
    DAT_007e11a8 = 0;
    FUN__text__00439e30(0xd);
    break;
  case 2:
    *(undefined4 *)(DAT_007a4a00 + 0x8e0) = 1;
    FUN__text__00422360(0);
    break;
  case 3:
    FUN__text__00439e30(0xe);
    break;
  case 4:
    FUN__text__00439e30(3);
    break;
  case 6:
    FUN__text__00439e30(0);
  }
  local_8 = 0x45ed98;
  FUN__text__0056ce80();
  return;
}

