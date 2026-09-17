
void __thiscall FUN__text__0048d490(int param_1,int param_2)

{
  undefined4 *puVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_10 = param_1 + 0x113a60;
  local_c = param_2;
  local_18 = (uint)*(byte *)(param_2 + 0xc);
  local_14 = 0;
  local_8 = param_1;
  do {
    if (local_14 == *(int *)(local_c + 0x48)) {
      *(undefined4 *)(local_10 + 8) = 0x4c;
      *(int *)(local_10 + 8) = *(int *)(local_10 + 8) + *(int *)(local_10 + 0x48) * 0x10;
      *(undefined4 *)(local_10 + 0x18 + local_18 * 4) =
           *(undefined4 *)(local_c + 0x18 + local_18 * 4);
      *(undefined4 *)(local_10 + 0x28 + local_18 * 4) =
           *(undefined4 *)(local_c + 0x28 + local_18 * 4);
      *(undefined4 *)(local_10 + 0x38 + local_18 * 4) =
           *(undefined4 *)(local_c + 0x38 + local_18 * 4);
      local_8 = 0x48d5c9;
      FUN__text__0056ce80();
      return;
    }
    puVar4 = (undefined4 *)(local_c + 0x4c + local_14 * 0x10);
    puVar1 = (undefined4 *)(local_10 + 0x4c + *(int *)(local_10 + 0x48) * 0x10);
    *puVar1 = *puVar4;
    puVar1[1] = puVar4[1];
    puVar1[2] = puVar4[2];
    puVar1[3] = puVar4[3];
    *(int *)(local_10 + 0x48) = *(int *)(local_10 + 0x48) + 1;
    if (0x1ff < *(int *)(local_10 + 0x48)) {
      iVar3 = FUN__text__00424f80("merge->cnt < 512",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618f90 + 0xd,0);
      if (iVar3 != 0) {
        pcVar2 = (code *)swi(3);
        (*pcVar2)();
        return;
      }
    }
    local_14 = local_14 + 1;
  } while( true );
}

