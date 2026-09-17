
void __fastcall FUN__text__004c1aa0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  undefined2 local_1c;
  undefined2 local_18;
  short local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  local_14 = 0;
  *(undefined2 *)(param_1 + 0x30) = 0;
  if (DAT_007f4491 == '\0') {
    if ((DAT_007a528e == 0xf) && (DAT_007a5290 == 4)) {
      *(undefined2 *)(param_1 + 0x30) = 2;
    }
  }
  else {
    *(undefined2 *)(param_1 + 0x30) = 1;
  }
  local_8 = param_1;
  FUN__text__004bd870();
  local_20 = (int)*(short *)(local_8 + 0x30);
  if (local_20 == 0) {
    local_c = FUN__text__004bdac0();
    FUN__text__004c1350();
    FUN__text__004d0750();
    FUN__text__00422360(5);
    local_18 = FUN__text__004d1ba0(*(short *)(&DAT_007cf46c + DAT_007e1180 * 0x124) + 1,0,5);
    *(undefined2 *)(&DAT_007cf46c + DAT_007e1180 * 0x124) = local_18;
    local_14 = 0;
  }
  else if (local_20 == 1) {
    FUN__text__004d0750();
    FUN__text__00422360(5);
    if (DAT_007f4505 == '\0') {
      local_14 = 4;
    }
    else {
      local_14 = 2;
    }
  }
  else if (local_20 == 2) {
    FUN__text__004c1350();
    FUN__text__004d0750();
    FUN__text__00422360(5);
    local_1c = FUN__text__004d1ba0(*(short *)(&DAT_007cf46c + DAT_007e1180 * 0x124) + 1,0,5);
    *(undefined2 *)(&DAT_007cf46c + DAT_007e1180 * 0x124) = local_1c;
    FUN__text__004d3510();
    local_14 = 3;
  }
  local_24 = (int)local_14;
  switch(local_24) {
  case 0:
    FUN__text__004ce210("Data\\Adv\\dat\\CH003.ybc",7);
    FUN__text__00439e30(6);
    break;
  default:
    FUN__text__00439e30(7);
    break;
  case 2:
    DAT_007e11a8 = 3;
    FUN__text__00439e30(0xd);
    break;
  case 3:
    FUN__text__004ce210("Data\\Adv\\dat\\CH003.ybc",0x12);
    FUN__text__00439e30(6);
    break;
  case 4:
    FUN__text__00439e30(0xf);
  }
  local_8 = 0x4c1d16;
  FUN__text__0056ce80();
  return;
}

