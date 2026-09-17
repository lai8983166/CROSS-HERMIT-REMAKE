
void FUN__text__0044a6e0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined2 local_1c;
  undefined *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(&DAT_007f4518,0,0x3700);
  local_c = (int)DAT_007a5260;
  local_18 = &DAT_007a5210;
  FUN__text__0044a7f0();
  local_18 = (undefined *)(local_8 + 0x1be0);
  local_14 = 0;
  local_10 = 0;
  do {
    if (local_14 == local_c) {
LAB__text__0044a7bf:
      FUN__text__0044aa30(local_10);
      FUN__text__0044aaf0();
      *(undefined1 *)(local_8 + 0x1a99) = 1;
      local_8 = 0x44a7ec;
      FUN__text__0056ce80();
      return;
    }
    local_1c = *(undefined2 *)((int)local_18 + local_14 * 2);
    FUN__text__004b9340(local_1c,CONCAT22((short)((uint)local_14 >> 0x10),(undefined2)local_10));
    local_10 = local_10 + 1;
    if (0x1d < local_10) goto LAB__text__0044a7bf;
    if (0x27 < local_10) {
      iVar2 = FUN__text__00424f80(&DAT_00598464,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606764 + 0x1a,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0044a7bf;
    }
    local_14 = local_14 + 1;
  } while( true );
}

