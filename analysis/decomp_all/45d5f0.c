
/* WARNING: Removing unreachable block (ram,0x0045dc7b) */

void __fastcall FUN__text__0045d5f0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = 0;
  local_8 = param_1;
  do {
    local_18 = local_10;
    if (local_10 == 0) {
      for (local_14 = 0; local_14 != 0x1c; local_14 = local_14 + 1) {
        FUN__text__004077c0(DAT_007a49fc);
      }
      FUN__text__004091a0(".\\data\\Command_Base255.bmp",1,0);
      FUN__text__004091a0(".\\data\\Menu255.bmp",1,0);
      FUN__text__004091a0(".\\data\\FileButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\GameButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\ConfigButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\FaceButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\StatusButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\ReportButton255.bmp",1,0);
      FUN__text__004091a0(".\\data\\020828_A256.bmp",1,0);
      FUN__text__004091a0(".\\data\\MiniMap255.bmp",1,0);
      FUN__text__004091a0(".\\data\\Search255.bmp",1,1);
      FUN__text__004091a0(".\\data\\Skill255.bmp",1,0);
      FUN__text__004091a0(".\\data\\AI255.bmp",1,0);
      FUN__text__004091a0(".\\data\\Face255.bmp",1,0);
      FUN__text__004091a0(".\\data\\char\\a0a00_1_00.bmp",1,0);
      FUN__text__004091a0(".\\data\\char\\a0a00_7_00.bmp",1,0);
      FUN__text__004091a0(".\\data\\char\\a0a01_1_00.bmp",1,0);
      FUN__text__004091a0(".\\data\\char\\a0a01_2_00.bmp",1,0);
      local_10 = local_10 + 1;
    }
    else if (local_10 == 1) {
      local_10 = 2;
    }
    else if (local_10 == 2) {
      FUN__text__004079c0(0,0);
      FUN__text__004079c0(0,0x259);
      FUN__text__004079c0(0,0);
      FUN__text__004079c0(3,2);
      FUN__text__004079c0(0x3c,2);
      FUN__text__004079c0(0x7e,2);
      FUN__text__004079c0(0x337,2);
      FUN__text__004079c0(0x387,2);
      FUN__text__004079c0(0x3bd,2);
      FUN__text__004079c0(800,0x26f);
      FUN__text__004079c0(0x2f0,0x26f);
      FUN__text__004079c0(0x2f0,0x29a);
      FUN__text__004079c0(0x2f0,0x2c5);
      FUN__text__004079c0(0x3cf,0x26f);
      FUN__text__004079c0(0x3cf,0x29a);
      FUN__text__004079c0(0x3cf,0x2c5);
      FUN__text__004079c0(0x19e,0x260);
      FUN__text__004079c0(0x1c4,0x260);
      FUN__text__004079c0(0x1ea,0x260);
      FUN__text__004079c0(0x210,0x260);
      FUN__text__004079c0(0x246,0x260);
      FUN__text__004079c0(0x26c,0x260);
      FUN__text__004079c0(0x292,0x260);
      FUN__text__004079c0(0x2b8,0x260);
      FUN__text__004079c0(0x19e,0x289);
      FUN__text__004079c0(0x1c4,0x289);
      FUN__text__004079c0(0x1ea,0x289);
      FUN__text__004079c0(0x210,0x289);
      FUN__text__004079c0(0x246,0x289);
      FUN__text__004079c0(0x26c,0x289);
      FUN__text__004079c0(0x292,0x289);
      FUN__text__004079c0(0x2b8,0x289);
      FUN__text__004079c0(0,0x1d);
      FUN__text__004079c0(0,0x56);
      FUN__text__004079c0(0,0x8f);
      FUN__text__004079c0(0,200);
      FUN__text__004079c0(0,0x101);
      FUN__text__004079c0(0,0x13a);
      FUN__text__004079c0(0,0x173);
      FUN__text__004079c0(0,0x1ac);
      FUN__text__004079c0(0,0x1e5);
      FUN__text__004079c0(0,0x21e);
      for (local_14 = 0; local_14 != 0x14; local_14 = local_14 + 1) {
        FUN__text__004079c0(local_14 * 0x20 + 0x40,0x40);
        FUN__text__004079c0(local_14 * 0x20 + 0x40,0x80);
        FUN__text__004079c0(local_14 * 0x20 + 0x40,0xc0);
        FUN__text__004079c0(local_14 * 0x20 + 0x40,0x100);
      }
    }
    local_c = local_c + 1;
    FUN__text__00422360(0);
  } while( true );
}

