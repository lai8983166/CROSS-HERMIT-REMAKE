
/* WARNING: Removing unreachable block (ram,0x0045e5b6) */

void __fastcall FUN__text__0045e3a0(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_d8 [16];
  undefined1 local_98 [128];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_d8;
  for (iVar2 = 0x35; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 0xd; local_c = local_c + 1) {
    uVar1 = FUN__text__004500b0((&PTR_s_data_sound_plw_unit001_plw_0060ce54)[local_c]);
    local_10 = FUN__text__0042ae20(uVar1);
    FUN__text__0042b2d0("%s : %08x\n",(&PTR_s_data_sound_plw_unit001_plw_0060ce54)[local_c],local_10
                       );
    FUN__text__0040c610(local_c + 7,local_10);
  }
  local_14 = 0;
  local_18 = 0;
  while( true ) {
    FUN__text__00422360(0);
    FUN__text__0056d810(local_98,"tbl = %d : offset = %d",local_14,local_18);
    FUN__text__0040ec50(0,0x40,1,0xffffffff,0,local_98);
    iVar2 = FUN__text__004128f0(0x39,1);
    if (iVar2 != 0) break;
    iVar2 = FUN__text__004128f0(0x1c,1);
    if (iVar2 != 0) {
      FUN__text__0040d390(local_14,local_18,0xffffffff,0);
    }
    iVar2 = FUN__text__004128f0(200,1);
    if (iVar2 != 0) {
      local_14 = local_14 + 1;
    }
    iVar2 = FUN__text__004128f0(0xd0,1);
    if (iVar2 != 0) {
      local_14 = local_14 + -1;
    }
    iVar2 = FUN__text__004128f0(0xcb,1);
    if (iVar2 != 0) {
      local_18 = local_18 + -1;
    }
    iVar2 = FUN__text__004128f0(0xcd,1);
    if (iVar2 != 0) {
      local_18 = local_18 + 1;
    }
    if (local_14 < 0) {
      local_14 = 0;
    }
    if (local_18 < 0) {
      local_18 = 0;
    }
  }
  do {
    FUN__text__00422360(0);
  } while( true );
}

