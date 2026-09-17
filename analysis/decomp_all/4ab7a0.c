
void FUN__text__004ab7a0(void)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__004a5ce0();
  *(undefined2 *)(local_8 + 0x76bc) = 0;
  *(undefined2 *)(local_8 + 0x76be) = 1;
  *(undefined2 *)(local_8 + 0x76c0) = 1;
  do {
    uVar1 = FUN__text__004a7c40();
    local_c = CONCAT22(local_c._2_2_,uVar1);
    FUN__text__00422360(0);
    local_10 = (local_c & 0xffff) - 1;
    switch(local_10) {
    case 0:
      *(undefined2 *)(local_8 + 0x76bc) = 2;
      *(undefined2 *)(local_8 + 0x76c0) = 0;
      break;
    case 1:
      *(undefined2 *)(local_8 + 0x76bc) = 3;
      *(undefined2 *)(local_8 + 0x76c0) = 0;
      break;
    case 2:
      *(undefined2 *)(local_8 + 0x76bc) = 1;
      *(undefined2 *)(local_8 + 0x76c0) = 0;
      break;
    case 6:
      *(undefined2 *)(local_8 + 0x76bc) = 4;
      *(undefined2 *)(local_8 + 0x76c0) = 0;
      break;
    case 7:
      FUN__text__004a6a10();
      *(undefined2 *)(local_8 + 0x76bc) = 0;
      *(undefined2 *)(local_8 + 0x76c0) = 0;
      if ((DAT_007a528e == 0xf) && (DAT_007a5290 == 5)) {
        FUN__text__0049ee30();
        *(undefined2 *)(local_8 + 0x76bc) = 5;
      }
    }
  } while (*(short *)(local_8 + 0x76c0) != 0);
  DAT_007a4e60 = 99;
  local_14 = (int)*(short *)(local_8 + 0x76bc);
  switch(local_14) {
  case 0:
    FUN__text__004db230(0x5a);
    while (iVar2 = FUN__text__004db270(), iVar2 == 0) {
      FUN__text__00422360(0);
    }
    FUN__text__004db120();
    FUN__text__00439e30(10);
    FUN__text__0041d280();
    break;
  case 1:
    FUN__text__00439e30(8);
    break;
  case 2:
    FUN__text__00439e30(0xd);
    break;
  case 3:
    FUN__text__00439e30(0xd);
    break;
  case 4:
    FUN__text__00439e30(1);
    break;
  case 5:
    FUN__text__00439e30(7);
  }
  FUN__text__004d6710();
  FUN__text__00422360(0);
  local_8 = 0x4aba29;
  FUN__text__0056ce80();
  return;
}

