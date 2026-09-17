
/* WARNING: Removing unreachable block (ram,0x0045e042) */

void FUN__text__0045dc90(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_e4 [16];
  int local_a4;
  int local_a0;
  char local_9c;
  int local_98;
  ushort local_3c;
  undefined4 local_38;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  char local_2d;
  undefined2 local_24;
  undefined2 local_22;
  undefined2 local_1e;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058fa3c;
  local_10 = ExceptionList;
  puVar3 = local_e4;
  for (iVar2 = 0x35; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  local_98 = 0;
  local_9c = '\0';
  FUN__text__004150a0(0);
  FUN__text__004143a0(0,0,0);
  local_a0 = FUN__text__0042ae20("data\\TACTICS\\Test\\MagTest.bin");
  if ((local_a0 == 0) &&
     (iVar2 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TestTask.cpp",
                                  DAT_0060ce98 + 0xb,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN__text__00416790(local_a0,1);
  do {
    local_9c = local_9c + '\x01';
    iVar2 = FUN__text__004128f0(0x1c,1);
    if (iVar2 != 0) {
      local_98 = (local_98 + 1) % 6;
    }
    local_a4 = local_98;
    switch(local_98) {
    case 0:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = -1;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 0;
      local_3c = 0;
      FUN__text__00407870(1,0);
      FUN__text__004079c0(0,0);
      break;
    case 1:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = -1;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 0;
      FUN__text__00407870(1,1);
      local_3c = local_3c | 1;
      local_24 = 200;
      local_22 = 200;
      FUN__text__004079c0(0,0);
      break;
    case 2:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = -1;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 0;
      FUN__text__00407870(1,2);
      local_3c = local_3c | 1;
      local_24 = 400;
      local_22 = 400;
      FUN__text__004079c0(0,0);
      break;
    case 3:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = local_9c;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 1;
      local_3c = 0;
      FUN__text__00407870(1,0);
      FUN__text__004079c0(0,0);
      break;
    case 4:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = local_9c;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 1;
      FUN__text__00407870(1,1);
      local_3c = local_3c | 1;
      local_24 = 200;
      local_22 = 200;
      FUN__text__004079c0(0,0);
      break;
    case 5:
      FUN__text__004077c0(DAT_007a49fc);
      local_1e = 1;
      local_2d = local_9c;
      local_2e = 0x80;
      local_2f = 0x80;
      local_30 = 0x80;
      local_38 = 1;
      FUN__text__00407870(1,2);
      local_3c = local_3c | 1;
      local_24 = 400;
      local_22 = 400;
      FUN__text__004079c0(0,0);
    }
    FUN__text__00422360(0);
  } while( true );
}

