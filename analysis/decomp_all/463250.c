
void FUN__text__00463250(void)

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
  local_10 = FUN__text__00463450();
  local_c = local_10;
  switch(local_10) {
  case 0:
    FUN__text__004e1b60();
    DAT_007f4488 = 0x4e;
    FUN__text__004da860(0x4e);
    FUN__text__00439e30(0x10);
    break;
  case 1:
    FUN__text__004e1b60();
    DAT_007f4488 = 0x4f;
    FUN__text__004da860(0x4f);
    FUN__text__00439e30(0x10);
    break;
  case 2:
    *(undefined4 *)(DAT_007a4a00 + 0x8e0) = 1;
    FUN__text__00422360(0);
    break;
  case 3:
    FUN__text__00439e30(0xe);
    break;
  case 4:
    FUN__text__004e1b60();
    DAT_007f4488 = 0x50;
    FUN__text__004da860(0x50);
    FUN__text__00439e30(0x10);
    break;
  case 5:
    FUN__text__00439e30(3);
    break;
  case 6:
    FUN__text__004e1b60();
    DAT_007f4488 = 0x4c;
    FUN__text__004da860(0x4c);
    FUN__text__00439e30(0x10);
    break;
  case 7:
    FUN__text__004e1b60();
    DAT_007f4488 = 0x4d;
    FUN__text__004da860(0x4d);
    FUN__text__00439e30(0x10);
    break;
  case 8:
    FUN__text__00439e30(0);
  }
  local_8 = 0x4633e9;
  FUN__text__0056ce80();
  return;
}

