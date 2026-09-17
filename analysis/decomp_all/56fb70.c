
undefined4 FUN_0056fb70(void)

{
  code *pcVar1;
  bool bVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *unaff_FS_OFFSET;
  char *local_30;
  undefined4 *local_24;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9b08;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  if ((DAT_007619c0 & 1) == 0) {
    *unaff_FS_OFFSET = uStack_14;
    return 1;
  }
  FUN_00577040(9);
  local_8 = 0;
  iVar3 = __heapchk();
  if ((iVar3 == -1) || (iVar3 == -2)) {
    for (local_24 = DAT_0080a438; local_24 != (undefined4 *)0x0; local_24 = (undefined4 *)*local_24)
    {
      bVar2 = true;
      if (((((local_24[5] & 0xffff) == 4) || (local_24[5] == 1)) || ((local_24[5] & 0xffff) == 2))
         || (local_24[5] == 3)) {
        local_30 = (&PTR_DAT_007619d0)[local_24[5] & 0xffff];
      }
      else {
        local_30 = "DAMAGED";
      }
      iVar3 = FUN_0056fae0(local_24 + 7,DAT_007619cc,4);
      if (iVar3 == 0) {
        iVar3 = FUN_00573780(0,0,0,0,"DAMAGE: before %hs block (#%d) at 0x%08X.\n",local_30,
                             local_24[6],local_24 + 8);
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
        bVar2 = false;
      }
      iVar3 = FUN_0056fae0((int)local_24 + local_24[4] + 0x20,DAT_007619cc,4);
      if (iVar3 == 0) {
        iVar3 = FUN_00573780(0,0,0,0,"DAMAGE: after %hs block (#%d) at 0x%08X.\n",local_30,
                             local_24[6],local_24 + 8);
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
        bVar2 = false;
      }
      if ((local_24[5] == 0) &&
         (iVar3 = FUN_0056fae0(local_24 + 8,DAT_007619cd,local_24[4]), iVar3 == 0)) {
        iVar3 = FUN_00573780(0,0,0,0,"DAMAGE: on top of Free block at 0x%08X.\n",local_24 + 8);
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
        bVar2 = false;
      }
      if (!bVar2) {
        if ((local_24[2] != 0) &&
           (iVar3 = FUN_00573780(0,0,0,0,"%hs allocated at file %hs(%d).\n",local_30,local_24[2],
                                 local_24[3]), iVar3 == 1)) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
        iVar3 = FUN_00573780(0,0,0,0,"%hs located at 0x%08X is %u bytes long.\n",local_30,
                             local_24 + 8,local_24[4]);
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
      }
    }
  }
  else {
    switch(iVar3) {
    case -6:
      iVar3 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_heapchk fails with _HEAPBADPTR.\n");
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      break;
    case -5:
      iVar3 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_heapchk fails with _HEAPBADEND.\n");
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      break;
    case -4:
      iVar3 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_heapchk fails with _HEAPBADNODE.\n");
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      break;
    case -3:
      iVar3 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_heapchk fails with _HEAPBADBEGIN.\n");
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
      break;
    default:
      iVar3 = FUN_00573780(0,0,0,0,&DAT_00592a18,"_heapchk fails with unknown return value!\n");
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        uVar4 = (*pcVar1)();
        return uVar4;
      }
    }
  }
  local_8 = 0xffffffff;
  FUN_0056fee5();
  uVar4 = FUN_0056fef0();
  return uVar4;
}

