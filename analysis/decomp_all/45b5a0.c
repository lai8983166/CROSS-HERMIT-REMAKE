
void FUN__text__0045b5a0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_2f4 [16];
  undefined4 local_2b4;
  undefined4 local_2b0;
  undefined4 local_2ac;
  uint local_2a8;
  undefined1 local_2a4 [512];
  int local_a4;
  int local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined2 local_24;
  undefined2 local_22;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f9fc;
  local_10 = ExceptionList;
  puVar3 = local_2f4;
  for (iVar2 = 0xb9; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  local_9c = 0;
  local_a0 = 0;
  local_a4 = 0;
  local_2a8 = local_2a8 & 0xffffff00;
  uVar1 = FUN__text__004500b0("data\\Sound\\plw\\unit010.plw");
  local_2b0 = FUN__text__0042ae20(uVar1);
  local_98 = FUN__text__0040c610(0,local_2b0);
  local_2b4 = local_2b0;
  FUN__text__00428ad0(local_2b0);
  while (iVar2 = FUN__text__004128f0(1,1), iVar2 == 0) {
    local_2ac = 1;
    iVar2 = FUN__text__004128f0(0x2a,0);
    if (iVar2 != 0) {
      local_2ac = 0;
    }
    iVar2 = FUN__text__004128f0(0x1d,0);
    if (iVar2 != 0) {
      do {
        iVar2 = FUN__text__004150e0();
      } while (iVar2 == 0);
      do {
        iVar2 = FUN__text__004150e0();
      } while (iVar2 == 0);
      do {
        iVar2 = FUN__text__004150e0();
      } while (iVar2 == 0);
    }
    FUN__text__0056d810(local_2a4,"ANIME-NO : NO0 = %d : NO1 = %d : FLIP = %02x",local_a0,local_a4,
                        local_2a8 & 0xff);
    FUN__text__00416370(0,0x20,0,local_2a4,0xffffffff);
    uVar1 = FUN__text__0040b740();
    uVar1 = FUN__text__0040b6d0(uVar1);
    FUN__text__0056d810(local_2a4,"ALLOC = %6d : FREE = %6d",uVar1);
    FUN__text__00416370(0,0x30,0,local_2a4,0xffffffff);
    iVar2 = FUN__text__004128f0(200,2);
    if (iVar2 != 0) {
      local_a0 = local_a0 + 1;
    }
    iVar2 = FUN__text__004128f0(0xd0,2);
    if (iVar2 != 0) {
      local_a0 = local_a0 + -1;
    }
    iVar2 = FUN__text__004128f0(0xcb,2);
    if (iVar2 != 0) {
      local_a4 = local_a4 + -1;
    }
    iVar2 = FUN__text__004128f0(0xcd,2);
    if (iVar2 != 0) {
      local_a4 = local_a4 + 1;
    }
    iVar2 = FUN__text__004128f0(0x1c,1);
    if (iVar2 != 0) {
      FUN__text__0040d390(0,local_a0,0xffffffff,0);
    }
    iVar2 = FUN__text__004128f0(0x4f,1);
    if (iVar2 != 0) {
      local_24 = 100;
      local_22 = 100;
    }
    iVar2 = FUN__text__004128f0(0x50,1);
    if (iVar2 != 0) {
      local_24 = 200;
      local_22 = 200;
    }
    iVar2 = FUN__text__004128f0(0x51,1);
    if (iVar2 != 0) {
      local_24 = 400;
      local_22 = 400;
    }
    iVar2 = FUN__text__004128f0(0x4b,1);
    if (iVar2 != 0) {
      local_24 = 800;
      local_22 = 800;
    }
    iVar2 = FUN__text__004128f0(0x47,1);
    if (iVar2 != 0) {
      local_2a8 = local_2a8 ^ 1;
    }
    iVar2 = FUN__text__004128f0(0x48,1);
    if (iVar2 != 0) {
      local_2a8 = local_2a8 ^ 2;
    }
    FUN__text__00422360(0);
  }
  FUN__text__00464d30();
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x45b9d3;
  FUN__text__0056ce80();
  return;
}

