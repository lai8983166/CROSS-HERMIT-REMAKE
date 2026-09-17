
void __fastcall FUN__text__00450ac0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_15c [16];
  int local_11c;
  int local_118;
  uint local_114;
  undefined1 local_110 [260];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_15c;
  for (iVar1 = 0x56; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_114 = 0;
  local_118 = 0;
  local_8 = param_1;
  while( true ) {
    FUN__text__0056d810(local_110,&DAT_005988ac,local_118 + 0x41);
    (*API_KERNEL32_DLL_GetDriveTypeA)(local_110);
    local_c = FUN__text__0056ce80();
    local_11c = local_c + -1;
    switch(local_11c) {
    case 0:
      FUN__text__0042b2d0("%s : DRIVE_NO_ROOT_DIR\n",local_110);
      break;
    case 1:
      FUN__text__0042b2d0("%s : DRIVE_REMOVABLE\n",local_110);
      break;
    case 2:
      FUN__text__0042b2d0("%s : DRIVE_FIXED\n",local_110);
      break;
    case 3:
      FUN__text__0042b2d0("%s : DRIVE_REMOTE\n",local_110);
      break;
    case 4:
      local_114 = local_114 | 1 << ((byte)local_118 & 0x1f);
      FUN__text__0042b2d0("%s : DRIVE_CDROM\n",local_110);
      break;
    case 5:
      FUN__text__0042b2d0("%s : DRIVE_RAMDISK\n",local_110);
      break;
    default:
      FUN__text__0042b2d0("%s : DRIVE_UNKNOWN\n",local_110);
    }
    if (0x59 < local_118 + 0x41) break;
    local_118 = local_118 + 1;
  }
  local_8 = 0x450c51;
  FUN__text__0056ce80();
  return;
}

