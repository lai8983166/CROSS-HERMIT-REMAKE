
void __fastcall FUN__text__00481a60(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  iVar2 = FUN__text__0046a430(*(undefined4 *)(param_1 + 0x108b60));
  if (iVar2 != 1) {
    iVar2 = FUN__text__00424f80("IsUwPlayer(select_uw[0])==1",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                DAT_00618ed4 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = 0;
  do {
    if (local_c == *(int *)(local_8 + 0x108b50)) {
      FUN__text__0046f170();
      local_8 = 0x481b8c;
      FUN__text__0056ce80();
      return;
    }
    iVar2 = FUN__text__00468d10(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
    if (iVar2 != 0) {
      if (*(char *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 600) + 0xa4) !=
          *(char *)(local_8 + 0x2ef44)) {
        iVar2 = FUN__text__00424f80("select_uw[i]->data->player==PlayerNo",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                    DAT_00618ed4 + 8,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      iVar2 = FUN__text__0046a7a0(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
      if (iVar2 == 0) {
        *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 0x28c) = 0;
      }
    }
    local_c = local_c + 1;
  } while( true );
}

