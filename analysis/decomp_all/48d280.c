
void __thiscall FUN__text__0048d280(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  local_18 = 0;
  local_8 = param_1;
  do {
    if (local_18 == *(int *)(local_c + 0x48)) {
      *(int *)(*(int *)(local_8 + 0x117c38) + 0x188) =
           *(int *)(*(int *)(local_8 + 0x117c38) + 0x188) + *(int *)(local_c + 0x48);
      for (local_18 = 0; local_18 != 4; local_18 = local_18 + 1) {
        *(undefined4 *)(local_8 + 0x117c08 + local_18 * 4) =
             *(undefined4 *)(local_c + 0x18 + local_18 * 4);
        *(undefined4 *)(local_8 + 0x117c18 + local_18 * 4) =
             *(undefined4 *)(local_c + 0x28 + local_18 * 4);
        *(undefined4 *)(local_8 + 0x117c28 + local_18 * 4) =
             *(undefined4 *)(local_c + 0x38 + local_18 * 4);
      }
      local_8 = 0x48d3ed;
      FUN__text__0056ce80();
      return;
    }
    local_10 = FUN__text__00427d60();
    if (local_10 == 0) {
      iVar2 = FUN__text__00424f80("ldst!=0",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618f8c + 10,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_14 = *(undefined4 **)(local_10 + 8);
    puVar3 = (undefined4 *)(local_c + 0x4c + local_18 * 0x10);
    *local_14 = *puVar3;
    local_14[1] = puVar3[1];
    local_14[2] = puVar3[2];
    local_14[3] = puVar3[3];
    FUN__text__00427e30(local_10);
    FUN__text__00496690(local_c + 0x4c + local_18 * 0x10);
    local_18 = local_18 + 1;
  } while( true );
}

