
/* WARNING: Removing unreachable block (ram,0x0045e385) */

void __fastcall FUN__text__0045e1e0(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_158 [16];
  undefined *local_118;
  undefined1 local_114 [260];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_158;
  for (iVar2 = 0x55; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  local_c = 0;
  local_8 = param_1;
  do {
    iVar2 = FUN__text__004128f0(200,2);
    if (iVar2 != 0) {
      local_c = local_c + 1;
    }
    iVar2 = FUN__text__004128f0(0xd0,2);
    if (iVar2 != 0) {
      local_c = local_c + -1;
    }
    iVar2 = FUN__text__004128f0(0xcb,2);
    if (iVar2 != 0) {
      local_10 = local_10 + 1;
    }
    iVar2 = FUN__text__004128f0(0xcd,2);
    if (iVar2 != 0) {
      local_10 = local_10 + -1;
    }
    if (local_c < 0) {
      local_c = 0;
    }
    if (local_10 < 0) {
      local_10 = 0;
    }
    iVar2 = FUN__text__004128f0(0x1c,1);
    if (iVar2 != 0) {
      local_118 = (&PTR_PTR_00621988)[local_c];
      uVar4 = *(undefined4 *)(local_118 + local_10 * 4);
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\");
      FUN__text__0056d810(local_114,&DAT_00592b28,uVar1,uVar4);
      FUN__text__0041e190(local_114,0);
    }
    FUN__text__0056d810(local_114,"TNO = %d : ONO = %d",local_c,local_10);
    FUN__text__00416370(0,0x70,0,local_114,0xffffffff);
    FUN__text__00422360(0);
  } while( true );
}

