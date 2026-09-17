
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__00448a30(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  int local_14;
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  for (local_10 = 0; local_10 != 0x50; local_10 = local_10 + 1) {
    if (*(short *)(param_1 + 0x1c30 + local_10 * 0xb0) != 0) {
      local_14 = local_14 + 1;
    }
  }
  local_8 = param_1;
  _memset(&DAT_007f4518,0,0x3700);
  for (local_10 = 0; local_10 != local_14; local_10 = local_10 + 1) {
    puVar3 = (undefined4 *)(local_8 + 0x1c30 + local_10 * 0xb0);
    puVar4 = (undefined4 *)(&DAT_007f4518 + local_10 * 0xb0);
    for (iVar2 = 0x2c; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
  }
  local_18 = FUN__text__0044c270((int)*(short *)(local_8 + 0x1a88));
  DAT_007f4488 = (short)local_18;
  FUN__text__004da860((int)(short)local_18);
  DAT_007f448c._3_1_ = 0;
  DAT_007f4490 = FUN__text__0041ad60();
  DAT_007f4491 = 1;
  DAT_007f448c._1_1_ = (undefined1)local_14;
  _memset(&DAT_007f44e4,0,0x10);
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    (&DAT_007f44e4)[local_10] = *(undefined1 *)(local_8 + local_10 + 0x1a8c);
  }
  _DAT_007f44d0 = *(undefined4 *)(local_8 + 0x1aa8);
  if ((DAT_007f4488 != *(short *)(local_8 + 0x1aa4)) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606738 + 0x1f,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  _memset(&DAT_007f44f4,0,0x10);
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    (&DAT_007f44f4)[local_10] = *(undefined1 *)(local_8 + local_10 + 0x1aac);
  }
  local_c = (undefined1 *)FUN__text__0044c200((int)*(short *)(local_8 + 0x1a88));
  DAT_007f4504 = *local_c;
  DAT_007f4505 = *(undefined1 *)(local_8 + 0x1a99);
  local_1c = FUN__text__0041ae70();
  _memset(&DAT_007f44d4,0,0x10);
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    (&DAT_007f44d4)[local_10] = *(undefined1 *)(local_1c + local_10 * 0x88);
  }
  local_8 = 0x448cad;
  FUN__text__0056ce80();
  return;
}

