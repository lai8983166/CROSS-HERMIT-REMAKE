
/* WARNING: Removing unreachable block (ram,0x0045d2a1) */

void FUN__text__0045cef0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined1 *puVar6;
  undefined4 uVar7;
  undefined4 local_48c [16];
  undefined4 local_44c;
  undefined4 local_428;
  uint local_424;
  undefined4 local_420;
  undefined4 local_41c;
  undefined4 local_418;
  undefined4 local_414;
  int local_410;
  undefined4 local_40c;
  undefined1 local_408 [1024];
  int local_8;
  
  puVar3 = local_48c;
  for (iVar2 = 0x122; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_420 = 0;
  local_424 = 0;
  local_428 = 0;
  puVar3 = &DAT_0059ada4;
  puVar4 = &local_44c;
  for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  *(undefined2 *)puVar4 = *(undefined2 *)puVar3;
  *(undefined1 *)((int)puVar4 + 2) = *(undefined1 *)((int)puVar3 + 2);
  local_41c = 0x14;
  (*API_GDI32_DLL_CreateFontA)(0x14,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  local_40c = FUN__text__0056ce80();
  FUN__text__004143a0(0,0,0xff);
  FUN__text__00416370(0,0x20,0,&DAT_0059ad9c,0xffffff80);
  FUN__text__00422360(0);
  FUN__text__0056d810(local_408,&local_44c);
  FUN__text__004077c0(DAT_007a49fc);
  uVar7 = 2;
  puVar6 = local_408;
  uVar5 = local_40c;
  uVar1 = FUN__text__004142b0(local_40c,puVar6,2);
  FUN__text__00408e30(uVar1,uVar5,puVar6,uVar7);
  FUN__text__00406a10();
  (*API_GDI32_DLL_DeleteObject)(local_40c);
  FUN__text__0056ce80();
  local_418 = 0;
  local_414 = 0;
  do {
    iVar2 = FUN__text__004128f0(0x1c,1);
    if (iVar2 != 0) {
      local_424 = local_424 ^ 1;
    }
    *(undefined2 *)(local_8 + 0x22f6) = 0xff;
    if (local_424 == 0) {
      local_418 = 0;
      local_414 = 0;
      for (local_410 = 0; local_410 != 10; local_410 = local_410 + 1) {
        FUN__text__0056d810(local_408,&local_44c);
        FUN__text__004077c0(DAT_007a49fc);
        *(undefined4 *)(local_8 + 0x22dc) = 1;
        *(undefined1 *)(local_8 + 0x22e7) = 0xff;
        *(undefined1 *)(local_8 + 0x22e6) = 0xff;
        *(undefined1 *)(local_8 + 0x22e5) = 0xff;
        *(undefined1 *)(local_8 + 0x22e4) = 0xff;
        FUN__text__00408f90(100,0x1e0);
      }
    }
    else {
      *(undefined4 *)(local_8 + 0x22dc) = 1;
      *(undefined1 *)(local_8 + 0x22e7) = 0xff;
      *(undefined1 *)(local_8 + 0x22e6) = 0x80;
      *(undefined1 *)(local_8 + 0x22e5) = 0x80;
      *(undefined1 *)(local_8 + 0x22e4) = 0x80;
      FUN__text__004077c0(DAT_007a49fc);
      FUN__text__00407a50(300,200);
      FUN__text__00410310(300,200,0x100,0x100,0xfff,0xff808080,0);
    }
    FUN__text__00410310(100,100,0x40,0x40,0xfff,0xffff0000,1);
    FUN__text__00410310(0xa4,100,0x40,0x40,0xfff,0xff00ff00,1);
    FUN__text__00410310(0xe4,100,0x40,0x40,0xfff,0xff0000ff,1);
    iVar2 = FUN__text__004128f0(0x39,0);
    if (iVar2 != 0) {
      FUN__text__00416370(0,0x20,0xff,&DAT_0059ad9c,0xffffff80);
    }
    FUN__text__00422360(0);
  } while( true );
}

