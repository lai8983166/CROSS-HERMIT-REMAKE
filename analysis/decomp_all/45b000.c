
void FUN__text__0045b000(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_2f0 [16];
  int local_2b0;
  int local_2ac;
  uint local_2a8;
  undefined1 local_2a4 [512];
  int local_a4;
  int local_a0;
  undefined4 local_9c;
  int local_98;
  undefined1 local_94 [88];
  undefined2 local_3c;
  undefined2 local_24;
  undefined2 local_22;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f9dc;
  local_10 = ExceptionList;
  puVar4 = local_2f0;
  for (iVar3 = 0xb8; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  local_9c = 0;
  local_a0 = 0;
  local_a4 = 0;
  local_2a8 = local_2a8 & 0xffffff00;
  *(undefined4 *)(local_14 + 0x1ee4) = 10;
  local_98 = FUN__text__00416b80(local_14 + 0x1ebc,"data\\DxAnim\\Efct.bin");
  FUN__text__0040b960(0);
  if ((local_98 != 0) &&
     (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\TestTask.cpp",
                                  DAT_0060ce90 + 0x2a,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN__text__00409ef0(local_14 + 0x1f10);
  FUN__text__00409ff0(local_14 + 0x1f10,0,0,local_2a8 & 0xff);
  local_2b0 = 0;
  while (iVar3 = FUN__text__004128f0(1,1), iVar3 == 0) {
    local_2ac = 1;
    iVar3 = FUN__text__004128f0(0x2a,0);
    if (iVar3 != 0) {
      local_2ac = 0;
    }
    iVar3 = FUN__text__004128f0(0x1d,0);
    if (iVar3 != 0) {
      do {
        iVar3 = FUN__text__004150e0();
      } while (iVar3 == 0);
      do {
        iVar3 = FUN__text__004150e0();
      } while (iVar3 == 0);
      do {
        iVar3 = FUN__text__004150e0();
      } while (iVar3 == 0);
    }
    FUN__text__004077c0(DAT_007a49fc);
    local_3c = 1;
    if ((local_2ac != 0) && (iVar3 = FUN__text__0040a100(local_14 + 0x1f10), iVar3 == 0)) {
      local_2b0 = local_2b0 + 1;
    }
    FUN__text__0040a330(local_14 + 0x1f10,local_94,0x200,0x180,0x80);
    FUN__text__0056d810(local_2a4,"ANIME-NO : NO0 = %d : NO1 = %d : FLIP = %02x",local_a0,local_a4,
                        local_2a8 & 0xff);
    FUN__text__00416370(0,0x20,0,local_2a4,0xffffffff);
    uVar2 = FUN__text__0040b740();
    uVar2 = FUN__text__0040b6d0(uVar2);
    FUN__text__0056d810(local_2a4,"ALLOC = %6d : FREE = %6d",uVar2);
    FUN__text__00416370(0,0x30,0,local_2a4,0xffffffff);
    FUN__text__0056d810(local_2a4,"PLAY-TIME = %6d",local_2b0);
    FUN__text__00416370(0,0x40,0,local_2a4,0xffffffff);
    iVar3 = FUN__text__004128f0(200,2);
    if (iVar3 != 0) {
      local_a0 = local_a0 + 1;
    }
    iVar3 = FUN__text__004128f0(0xd0,2);
    if (iVar3 != 0) {
      local_a0 = local_a0 + -1;
    }
    iVar3 = FUN__text__004128f0(0xcb,2);
    if (iVar3 != 0) {
      local_a4 = local_a4 + -1;
    }
    iVar3 = FUN__text__004128f0(0xcd,2);
    if (iVar3 != 0) {
      local_a4 = local_a4 + 1;
    }
    if (local_a0 < 0) {
      local_a0 = 0;
    }
    if (local_a4 < 0) {
      local_a4 = 0;
    }
    if (3 < local_a0) {
      local_a0 = 3;
    }
    if (200 < local_a4) {
      local_a4 = 200;
    }
    iVar3 = FUN__text__004128f0(0x1c,1);
    if (iVar3 != 0) {
      FUN__text__00409ff0(local_14 + 0x1f10,local_a0,local_a4,local_2a8 & 0xff);
      local_2b0 = 0;
    }
    iVar3 = FUN__text__004128f0(0x4f,1);
    if (iVar3 != 0) {
      local_24 = 100;
      local_22 = 100;
    }
    iVar3 = FUN__text__004128f0(0x50,1);
    if (iVar3 != 0) {
      local_24 = 200;
      local_22 = 200;
    }
    iVar3 = FUN__text__004128f0(0x51,1);
    if (iVar3 != 0) {
      local_24 = 400;
      local_22 = 400;
    }
    iVar3 = FUN__text__004128f0(0x4b,1);
    if (iVar3 != 0) {
      local_24 = 800;
      local_22 = 800;
    }
    iVar3 = FUN__text__004128f0(0x47,1);
    if (iVar3 != 0) {
      local_2a8 = local_2a8 ^ 1;
    }
    iVar3 = FUN__text__004128f0(0x48,1);
    if (iVar3 != 0) {
      local_2a8 = local_2a8 ^ 2;
    }
    FUN__text__00422360(0);
  }
  FUN__text__00464d30();
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x45b59c;
  FUN__text__0056ce80();
  return;
}

