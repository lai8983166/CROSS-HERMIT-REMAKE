
void FUN_005705b0(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 *local_24;
  undefined4 *local_20;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9c98;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  local_24 = (undefined4 *)0x0;
  FUN_00577040(9);
  local_8 = 0;
  iVar2 = FUN_00573780(0,0,0,0,&DAT_00592a18,"Dumping objects ->\n");
  if (iVar2 == 1) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (param_1 != (undefined4 *)0x0) {
    local_24 = (undefined4 *)*param_1;
  }
  local_20 = DAT_0080a438;
  do {
    if ((local_20 == (undefined4 *)0x0) || (local_20 == local_24)) {
      local_8 = 0xffffffff;
      FUN_00570861();
      FUN_0057086c();
      return;
    }
    if ((((local_20[5] & 0xffff) != 3) && ((local_20[5] & 0xffff) != 0)) &&
       (((local_20[5] & 0xffff) != 2 || ((DAT_007619c0 & 0x10) != 0)))) {
      if (local_20[2] != 0) {
        iVar2 = ATL::AtlIsValidAddress((void *)local_20[2],1,0);
        if (iVar2 == 0) {
          iVar2 = FUN_00573780(0,0,0,0,"#File Error#(%d) : ",local_20[3]);
          if (iVar2 == 1) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else {
          iVar2 = FUN_00573780(0,0,0,0,"%hs(%d) : ",local_20[2],local_20[3]);
          if (iVar2 == 1) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
      iVar2 = FUN_00573780(0,0,0,0,"{%ld} ",local_20[6]);
      if (iVar2 == 1) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if ((local_20[5] & 0xffff) == 4) {
        iVar2 = FUN_00573780(0,0,0,0,"client block at 0x%08X, subtype %x, %u bytes long.\n",
                             local_20 + 8,(int)local_20[5] >> 0x10 & 0xffff,local_20[4]);
        if (iVar2 == 1) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        if (DAT_0080bb78 == (code *)0x0) {
          FUN_005708b0(local_20);
        }
        else {
          (*DAT_0080bb78)(local_20 + 8,local_20[4]);
        }
      }
      else if (local_20[5] == 1) {
        iVar2 = FUN_00573780(0,0,0,0,"normal block at 0x%08X, %u bytes long.\n",local_20 + 8,
                             local_20[4]);
        if (iVar2 == 1) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        FUN_005708b0(local_20);
      }
      else if ((local_20[5] & 0xffff) == 2) {
        iVar2 = FUN_00573780(0,0,0,0,"crt block at 0x%08X, subtype %x, %u bytes long.\n",
                             local_20 + 8,(int)local_20[5] >> 0x10 & 0xffff,local_20[4]);
        if (iVar2 == 1) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        FUN_005708b0(local_20);
      }
    }
    local_20 = (undefined4 *)*local_20;
  } while( true );
}

