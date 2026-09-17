
/* WARNING: Removing unreachable block (ram,0x0045afce) */

void FUN__text__0045ae00(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_ec [16];
  int local_ac;
  uint local_a8;
  uint local_a4;
  int local_a0;
  uint local_9c;
  undefined4 local_98;
  ushort local_3c;
  undefined2 local_24;
  undefined2 local_22;
  undefined2 local_1e;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f9bc;
  local_10 = ExceptionList;
  puVar2 = local_ec;
  for (iVar1 = 0x37; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  local_ac = 0;
  local_98 = FUN__text__004168e0(local_14 + 0x1ea8,"data\\TexPos\\TexPos.bin");
  do {
    FUN__text__004077c0(DAT_007a49fc);
    local_1e = 2;
    FUN__text__00407870(*(undefined4 *)(local_14 + 0x1eb8),local_ac);
    local_3c = local_3c | 1;
    local_9c = _rand();
    local_9c = local_9c & 0x800003ff;
    if ((int)local_9c < 0) {
      local_9c = (local_9c - 1 | 0xfffffc00) + 1;
    }
    local_a0 = _rand();
    local_a0 = local_a0 % 0x300;
    local_24 = 800;
    local_22 = 800;
    FUN__text__0041ed80(local_ac,&local_a4,&local_a8);
    FUN__text__004079c0((local_a4 & 0xffff) + 100,(local_a8 & 0xffff) + 100);
    iVar1 = FUN__text__004128f0(200,1);
    if (iVar1 != 0) {
      local_ac = local_ac + -1;
    }
    iVar1 = FUN__text__004128f0(0xd0,1);
    if (iVar1 != 0) {
      local_ac = local_ac + 1;
    }
    if (local_ac < 0) {
      local_ac = 0x55;
    }
    if (0x55 < local_ac) {
      local_ac = 0;
    }
    FUN__text__00422360(0);
  } while( true );
}

