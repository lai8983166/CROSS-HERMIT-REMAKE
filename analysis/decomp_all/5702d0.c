
void FUN_005702d0(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 *local_24;
  int local_20;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9b80;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  if (param_1 != (undefined4 *)0x0) {
    FUN_00577040(9);
    local_8 = 0;
    *param_1 = DAT_0080a438;
    for (local_20 = 0; local_20 < 5; local_20 = local_20 + 1) {
      param_1[local_20 + 6] = 0;
      param_1[local_20 + 1] = 0;
    }
    local_24 = DAT_0080a438;
    do {
      if (local_24 == (undefined4 *)0x0) {
        param_1[0xb] = DAT_0080a440;
        param_1[0xc] = DAT_0080a434;
        local_8 = 0xffffffff;
        FUN_00570458();
        FUN_00570463();
        return;
      }
      if ((local_24[5] & 0xffff) < 5) {
        param_1[(local_24[5] & 0xffff) + 1] = param_1[(local_24[5] & 0xffff) + 1] + 1;
        param_1[(local_24[5] & 0xffff) + 6] = param_1[(local_24[5] & 0xffff) + 6] + local_24[4];
      }
      else {
        iVar2 = FUN_00573780(0,0,0,0,"Bad memory block found at 0x%08X.\n",local_24);
        if (iVar2 == 1) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_24 = (undefined4 *)*local_24;
    } while( true );
  }
  iVar2 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_CrtMemCheckPoint: NULL state pointer.\n");
  if (iVar2 == 1) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN_00570463();
  return;
}

