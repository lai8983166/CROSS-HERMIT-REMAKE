
/* WARNING: Removing unreachable block (ram,0x0045ceb2) */

void FUN__text__0045c5d0(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined1 *puVar5;
  undefined4 uVar6;
  undefined4 local_4bc [16];
  int local_47c;
  char *local_478 [4];
  char *local_468;
  char *local_464;
  char *local_460;
  char *local_45c;
  char *local_458;
  char *local_454;
  int local_450;
  uint local_44c;
  undefined4 local_448;
  undefined4 local_444;
  int local_440;
  undefined4 local_43c;
  int local_438;
  int local_434;
  undefined4 local_430 [10];
  undefined1 local_408 [1024];
  int local_8;
  
  puVar4 = local_4bc;
  for (iVar3 = 0x12e; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_448 = 0;
  local_44c = 0;
  local_450 = 0;
  local_478[0] = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_478[1] = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_478[2] = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_478[3] = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_468 = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_464 = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_460 = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_45c = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_458 = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_454 = 
  "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
  ;
  local_444 = 100;
  for (local_438 = 0; local_438 != 10; local_438 = local_438 + 1) {
    (*API_GDI32_DLL_CreateFontA)(0x14,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
    uVar1 = FUN__text__0056ce80();
    local_430[local_438] = uVar1;
  }
  FUN__text__004150a0(0);
  FUN__text__004143a0(0,0,0xff);
  for (local_438 = 0; local_438 != 10; local_438 = local_438 + 1) {
    FUN__text__0056d810(local_408,local_478[local_438]);
    FUN__text__004077c0(DAT_007a49fc);
    uVar6 = 2;
    puVar5 = local_408;
    uVar1 = local_430[local_438];
    uVar2 = FUN__text__004142b0(uVar1,puVar5,2);
    FUN__text__00408e30(uVar2,uVar1,puVar5,uVar6);
  }
  local_440 = 0;
  local_43c = 0;
  local_434 = 0;
  do {
    local_434 = local_434 + 1;
    iVar3 = FUN__text__004128f0(0x1c,1);
    if (iVar3 != 0) {
      local_44c = local_44c ^ 1;
    }
    iVar3 = FUN__text__004128f0(0x52,1);
    if (iVar3 != 0) {
      local_450 = 0;
    }
    iVar3 = FUN__text__004128f0(0x4f,1);
    if (iVar3 != 0) {
      local_450 = 1;
    }
    iVar3 = FUN__text__004128f0(0x50,1);
    if (iVar3 != 0) {
      local_450 = 2;
    }
    iVar3 = FUN__text__004128f0(0x51,1);
    if (iVar3 != 0) {
      local_450 = 3;
    }
    iVar3 = FUN__text__004128f0(0x4b,1);
    if (iVar3 != 0) {
      local_450 = 4;
    }
    iVar3 = FUN__text__004128f0(0x4c,1);
    if (iVar3 != 0) {
      local_450 = 5;
    }
    iVar3 = FUN__text__004128f0(0x4d,1);
    if (iVar3 != 0) {
      local_450 = 6;
    }
    iVar3 = FUN__text__004128f0(0x47,1);
    if (iVar3 != 0) {
      local_450 = 7;
    }
    iVar3 = FUN__text__004128f0(0x48,1);
    if (iVar3 != 0) {
      local_450 = 8;
    }
    iVar3 = FUN__text__004128f0(0x49,1);
    if (iVar3 != 0) {
      local_450 = 9;
    }
    if (local_44c == 0) {
      local_440 = 0;
      local_43c = 0;
      for (local_438 = 0; local_438 != 10; local_438 = local_438 + 1) {
        FUN__text__0056d810(local_408,local_478[local_438]);
        FUN__text__004077c0(DAT_007a49fc);
        local_47c = local_438;
        switch(local_438) {
        case 0:
          *(undefined4 *)(local_8 + 0x22dc + local_438 * 0x80) = 1;
          *(char *)(local_8 + 0x22e7 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e7 + local_438 * 0x80) + '\x01';
          *(undefined1 *)(local_8 + 0x22e6 + local_438 * 0x80) = 0xff;
          *(undefined1 *)(local_8 + 0x22e5 + local_438 * 0x80) = 0xff;
          *(undefined1 *)(local_8 + 0x22e4 + local_438 * 0x80) = 0xff;
          FUN__text__0056d810(local_408,&DAT_0059ad00,local_434);
          uVar6 = 2;
          puVar5 = local_408;
          uVar1 = local_430[0];
          uVar2 = FUN__text__004142b0(local_430[0],puVar5,2);
          FUN__text__00408e30(uVar2,uVar1,puVar5,uVar6);
          break;
        case 1:
          *(undefined4 *)(local_8 + 0x22dc + local_438 * 0x80) = 0;
          *(char *)(local_8 + 0x22e6 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e6 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e5 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e5 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e4 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e4 + local_438 * 0x80) + '\x01';
          break;
        case 2:
          *(undefined4 *)(local_8 + 0x22dc + local_438 * 0x80) = 1;
          *(char *)(local_8 + 0x22e7 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e7 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e6 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e6 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e5 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e5 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e4 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e4 + local_438 * 0x80) + '\x01';
          break;
        case 3:
          *(char *)(local_8 + 0x22e6 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e6 + local_438 * 0x80) + '\x01';
          break;
        case 4:
          *(char *)(local_8 + 0x22e5 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e5 + local_438 * 0x80) + '\x01';
          break;
        case 5:
          *(char *)(local_8 + 0x22e4 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e4 + local_438 * 0x80) + '\x01';
          break;
        case 6:
          *(char *)(local_8 + 0x22e6 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e6 + local_438 * 0x80) + '\x01';
          *(char *)(local_8 + 0x22e5 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e5 + local_438 * 0x80) + '\x02';
          *(char *)(local_8 + 0x22e4 + local_438 * 0x80) =
               *(char *)(local_8 + 0x22e4 + local_438 * 0x80) + '\x03';
          break;
        default:
          *(undefined1 *)(local_8 + 0x22e6 + local_438 * 0x80) = 0xff;
          *(undefined1 *)(local_8 + 0x22e5 + local_438 * 0x80) = 0xff;
          *(undefined1 *)(local_8 + 0x22e4 + local_438 * 0x80) = 0xff;
        }
        FUN__text__00408f90(local_43c,local_440 + 0x50);
        local_440 = local_440 + *(short *)(local_8 + 0x22c2 + local_438 * 0x80);
      }
    }
    else {
      *(undefined4 *)(local_8 + 0x22dc + local_450 * 0x80) = 0;
      *(undefined1 *)(local_8 + 0x22e7 + local_450 * 0x80) = 0xff;
      *(undefined1 *)(local_8 + 0x22e6 + local_450 * 0x80) = 0x80;
      *(undefined1 *)(local_8 + 0x22e5 + local_450 * 0x80) = 0x80;
      *(undefined1 *)(local_8 + 0x22e4 + local_450 * 0x80) = 0x80;
      FUN__text__004077c0(DAT_007a49fc);
      FUN__text__00407a50(300,200);
      FUN__text__00410310(300,200,0x100,0x100,0,0xff808080,0);
    }
    FUN__text__00422360(0);
  } while( true );
}

