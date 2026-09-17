
void __fastcall FUN__text__0048ceb0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  void *local_1c;
  int local_18;
  int local_14;
  undefined4 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  FUN__text__00416fa0(*(int *)(param_1 + 0x117c38) + 0x117df8);
  iVar2 = FUN__text__00419450();
  if (iVar2 == 0) {
    local_1c = (void *)(local_8 + 0x111a14);
    *(undefined4 *)(local_8 + 0x111a5c) = 0;
    _memset(local_1c,0,0x10);
    *(undefined1 *)((int)local_1c + 0xc) = *(undefined1 *)(local_8 + 0x2ef44);
    *(undefined1 *)((int)local_1c + 0xd) = 4;
    _memset((void *)((int)local_1c + 0x10),0,0x38);
    *(undefined4 *)((int)local_1c + (uint)*(byte *)(local_8 + 0x2ef44) * 4 + 0x18) =
         *(undefined4 *)(local_8 + 0x2e6f4);
    *(undefined4 *)((int)local_1c + (uint)*(byte *)(local_8 + 0x2ef44) * 4 + 0x28) =
         *(undefined4 *)(local_8 + 0x2e70c);
    *(undefined4 *)((int)local_1c + (uint)*(byte *)(local_8 + 0x2ef44) * 4 + 0x38) =
         *(undefined4 *)(local_8 + 0x2e710);
    while (local_c = FUN__text__00427de0(), local_c != 0) {
      local_10 = *(undefined4 **)(local_c + 8);
      puVar3 = (undefined4 *)((int)local_1c + *(int *)((int)local_1c + 0x48) * 0x10 + 0x4c);
      *puVar3 = *local_10;
      puVar3[1] = local_10[1];
      puVar3[2] = local_10[2];
      puVar3[3] = local_10[3];
      *(int *)((int)local_1c + 0x48) = *(int *)((int)local_1c + 0x48) + 1;
      if (0x1ff < *(int *)((int)local_1c + 0x48)) {
        iVar2 = FUN__text__00424f80("work->cnt < 512",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618f88 + 0x3a,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      FUN__text__00427e70(local_c);
    }
    *(undefined4 *)((int)local_1c + 8) = 0x4c;
    *(int *)((int)local_1c + 8) =
         *(int *)((int)local_1c + 8) + *(int *)((int)local_1c + 0x48) * 0x10;
    local_14 = FUN__text__00419f90(local_1c,*(undefined4 *)((int)local_1c + 8));
    if ((local_14 != 0) &&
       (iVar2 = FUN__text__00424f80("ret==0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618f88 + 0x43,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__00416ff0(*(int *)(local_8 + 0x117c38) + 0x117df8);
    FUN__text__00417050(*(int *)(local_8 + 0x117c38) + 0x117df8);
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x117f18) = *(undefined4 *)((int)local_1c + 0x48)
    ;
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x117f1c) = *(undefined4 *)((int)local_1c + 8);
  }
  else {
    FUN__text__0048d400();
    local_18 = local_8 + 0x113a60;
    while (local_c = FUN__text__00427de0(), local_c != 0) {
      local_10 = *(undefined4 **)(local_c + 8);
      puVar3 = (undefined4 *)(local_18 + 0x4c + *(int *)(local_18 + 0x48) * 0x10);
      *puVar3 = *local_10;
      puVar3[1] = local_10[1];
      puVar3[2] = local_10[2];
      puVar3[3] = local_10[3];
      *(int *)(local_18 + 0x48) = *(int *)(local_18 + 0x48) + 1;
      if (0x1ff < *(int *)(local_18 + 0x48)) {
        iVar2 = FUN__text__00424f80("merge->cnt < 512",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618f88 + 0x17,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      FUN__text__00427e70(local_c);
    }
    *(undefined4 *)(local_18 + 8) = 0x4c;
    *(int *)(local_18 + 8) = *(int *)(local_18 + 8) + *(int *)(local_18 + 0x48) * 0x10;
    FUN__text__00416ff0(*(int *)(local_8 + 0x117c38) + 0x117df8);
    FUN__text__00417050(*(int *)(local_8 + 0x117c38) + 0x117df8);
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x117f18) = *(undefined4 *)(local_18 + 0x48);
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x117f1c) = *(undefined4 *)(local_18 + 8);
  }
  local_8 = 0x48d278;
  FUN__text__0056ce80();
  return;
}

