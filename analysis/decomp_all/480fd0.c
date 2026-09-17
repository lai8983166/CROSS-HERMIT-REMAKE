
void __thiscall FUN__text__00480fd0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(char *)(*(int *)(param_2 + 600) + 0xa4) != *(char *)(param_1 + 0x2ef44)) {
    iVar2 = FUN__text__00424f80("wk->data->player==PlayerNo",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                DAT_00618ec0 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (undefined1 *)(local_8 + 0x108f48);
  FUN__text__00480f50(param_2);
  local_14 = 0;
  for (local_10 = 0; local_10 != *(int *)(local_8 + 0x108b50); local_10 = local_10 + 1) {
    iVar2 = FUN__text__0046a7a0(*(undefined4 *)(local_8 + 0x108b60 + local_10 * 4));
    if (iVar2 != 0) {
      *(undefined2 *)(local_c + local_14 * 2 + 2) =
           *(undefined2 *)(*(int *)(local_8 + 0x108b60 + local_10 * 4) + 2);
      local_14 = local_14 + 1;
    }
  }
  *local_c = (undefined1)local_14;
  local_8 = 0x4810c5;
  FUN__text__0056ce80();
  return;
}

